import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def normalize_url(url):
    parsed = urlparse(url)
    combined = parsed.netloc + parsed.path
    if combined.endswith('/'):
        combined = combined[:-1]
    return combined

def extract_page_data(html, page_url):
    soup = BeautifulSoup(html, 'html.parser')
    h = soup.find('h1') or soup.find('h2')
    heading = h.get_text().strip() if h else ""
    main_tag = soup.find('main')
    p_tag = main_tag.find('p') if main_tag else soup.find('p')
    first_paragraph = p_tag.get_text().strip() if p_tag else ""
    
    outgoing_links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href:
            outgoing_links.append(urljoin(page_url, href))
            
    image_urls = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            image_urls.append(urljoin(page_url, src))
            
    return {
        "url": page_url, "heading": heading, "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links, "image_urls": image_urls
    }

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=5, max_pages=10):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            
            if normalized_url in self.page_data:
                return False

            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return False
            
            self.page_data[normalized_url] = None
            return True

    async def get_html(self, url):
        headers = {"User-Agent": "BootCrawler/1.0"}
        try:
            async with self.session.get(url, headers=headers, timeout=10) as response:
                if response.status >= 400 or "text/html" not in response.headers.get("Content-Type", ""):
                    return None
                return await response.text()
        except Exception:
            return None

    async def crawl_page(self, current_url):
        if self.should_stop:
            return

        if urlparse(current_url).netloc != self.base_domain:
            return

        norm_url = normalize_url(current_url)
        if not await self.add_page_visit(norm_url):
            return

        async with self.semaphore:
            print(f"Crawling: {current_url}")
            html = await self.get_html(current_url)
        
        if html is None or self.should_stop:
            return

        data = extract_page_data(html, current_url)
        async with self.lock:
            self.page_data[norm_url] = data

        for next_url in data["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(next_url))
            self.all_tasks.add(task)
            task.add_done_callback(self.all_tasks.discard)

    async def crawl(self):
        root_task = asyncio.create_task(self.crawl_page(self.base_url))
        self.all_tasks.add(root_task)
        root_task.add_done_callback(self.all_tasks.discard)
        
        while self.all_tasks:
            try:
                await asyncio.gather(*list(self.all_tasks))
            except asyncio.CancelledError:
                break
        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
