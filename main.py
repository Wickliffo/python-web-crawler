import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report

async def main_async():
    args = sys.argv
    if len(args) < 4:
        print("Usage: uv run main.py <URL> <max_concurrency> <max_pages>")
        sys.exit(1)
    
    base_url = args[1]
    max_concurrency = int(args[2])
    max_pages = int(args[3])
    
    print(f"--- STARTING CRAWL ---")
    print(f"Target: {base_url}")
    
    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    
    print(f"Crawl complete. Found {len(page_data)} pages.")
    
    # Export to JSON
    write_json_report(page_data)

if __name__ == "__main__":
    asyncio.run(main_async())
