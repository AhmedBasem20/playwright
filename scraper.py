import os
os.system("playwright install") 

from playwright.sync_api import sync_playwright
import time

def scrape_behance_images(url, max_scrolls=2, scroll_delay=2):
    image_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for production
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # Initial wait

        for _ in range(max_scrolls):
            page.mouse.wheel(0, 3000)
            time.sleep(scroll_delay)

        # Try multiple selectors to handle different lazy-load behaviors
        selectors = [
            'img[src^="https://mir-s3-cdn-cf"]',        # common behance CDN
            'img[src^="https://assets"]',
            'img[src^="https://pro2"]',
            'img[src]:not([src^="data:image"])',        # filter out base64 dummy
        ]

        for sel in selectors:
            for img in page.query_selector_all(sel):
                src = img.get_attribute("src")
                if src and "/user/" not in src:
                    image_urls.add(src)

        browser.close()

    return list(image_urls)


if __name__ == "__main__":
    query = "Beauty products"
    query = query.replace(" ", "%20")
    url = f"https://www.behance.net/search/images/{query}"
    urls = scrape_behance_images(url)
    
    print(f"\nFound {len(urls)} image URLs:\n")
    for u in urls:
        print(u)
