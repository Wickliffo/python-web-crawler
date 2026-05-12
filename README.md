# Asynchronous Web Crawler 🕷️

A high-performance, concurrent web crawler built with Python, `asyncio`, and `aiohttp`. This project demonstrates how to traverse complex web domains, manage state across concurrent tasks, and export structured data into a JSON report.

---

## 🚩 Problem Statement

Traditional web scrapers often operate **synchronously**, visiting one URL at a time. This creates a massive bottleneck: the CPU sits idle while waiting for network responses (I/O Bound). For a website with 1,000 pages, a synchronous crawler taking 1 second per page would require over 16 minutes to complete. 

Furthermore, naive crawlers risk:
1. **Infinite Loops:** Getting stuck in circular link structures.
2. **Resource Exhaustion:** Crashing the system by opening too many simultaneous connections.
3. **Data Inconsistency:** Race conditions when multiple tasks try to write to a shared data structure.

## 🎯 Objectives

The goal of this project was to build a production-grade crawler that:
*   **Maximizes Efficiency:** Uses asynchronous coroutines to handle multiple requests in parallel.
*   **Implements Safety:** Uses Semaphores to throttle concurrency and prevent IP blocking/server strain.
*   **Ensures Integrity:** Uses Thread-safe Locks to manage a central data repository.
*   **Provides Control:** Supports user-defined limits for maximum pages and concurrency levels.

## 🛠️ The Solution

This crawler is built using a Class-based Asynchronous architecture:

1.  **Async/Await Engine:** Utilizing `aiohttp` and `asyncio` to allow the program to "pause" and switch tasks while waiting for network responses.
2.  **Atomic State Management:** An `asyncio.Lock` ensures the shared dictionary (`page_data`) is never corrupted by simultaneous writes.
3.  **Concurrency Throttling:** An `asyncio.Semaphore` acts as a gatekeeper, ensuring only `N` requests are active at any given time.
4.  **Graceful Shutdown:** When the `max_pages` limit is hit, the crawler uses `Task.cancel()` to cleanly terminate all pending workers.
5.  **Normalized Persistence:** Data is normalized via `urllib.parse` and exported into a sorted, structured `report.json`.

---

## 🏗️ Project Structure

```text
web-crawler/
├── main.py          # Entry point; handles CLI arguments and event loop initialization.
├── crawl.py         # Core AsyncCrawler class, HTML parsing logic, and task management.
├── json_report.py   # Transformation logic for sorting and exporting data to JSON.
├── requirements.txt # Project dependencies (aiohttp, beautifulsoup4, requests).
└── report.json      # Final output generated after a successful crawl.
🚀 Getting Started
Prerequisites
Python 3.10+

uv (recommended) or pip

Installation
Clone the repository:

Bash
git clone [https://github.com/Wickliffo/python-web-crawler.git](https://github.com/Wickliffo/python-web-crawler.git)
cd python-web-crawler
Install dependencies:

Bash
uv pip install -r requirements.txt


### Usage
Run the crawler by providing a starting URL, concurrency limit, and page limit:
```bash
uv run main.py [https://example.com](https://example.com) 5 50
5: Maximum concurrent connections.

50: Maximum total pages to crawl.

📊 Sample Output (report.json)
JSON
[
  {
    "url": "[https://example.com/about](https://example.com/about)",
    "heading": "About Us",
    "first_paragraph": "We are a tech-focused company...",
    "outgoing_links": ["[https://example.com/contact](https://example.com/contact)"],
    "image_urls": ["[https://example.com/logo.png](https://example.com/logo.png)"]
  }
]
