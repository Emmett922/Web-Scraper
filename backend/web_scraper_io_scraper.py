# necessary imports
from selectolax.parser import HTMLParser
import asyncio
from playwright.async_api import async_playwright
from playwright._impl._errors import TargetClosedError
import os
from fasteners import InterProcessLock

# Method to parse HTML content and extract product information
def parse_item(html_page):
    results = []
    html = HTMLParser(html_page) # Parse the HTML content
    data = html.css("div.caption") # Select the product containers
    for item in data:
        product = {
            "title": item.css_first("a.title").text(), # Extract title
            "price": item.css_first("h4.price.float-end.pull-right").text(), # Extract price
            "descr": item.css_first("p.card-text.description").text() # Extract descr.
            }
        results.append(product) # Add the product data to the results list
    return results

# Method to perform the web scraping
async def run_scraper():
    url = "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops" # Target URL
    laptops = []
    
    try:
        async with async_playwright() as pw: # Start Playwright
            browser = await pw.chromium.launch(headless=False) # Launch Chromium browser
            page = await browser.new_page() # Open a new page
            await page.goto(url, wait_until="networkidle") # Navigate to the target URL
            
            while True:
                content = await page.content() # Get page content
                laptops.extend(parse_item(content)) # Parse and collect product data
                
                next_page = page.locator("button.next") # Locate the "Next" button on the page
                
                await page.wait_for_load_state("networkidle") # Wait for the page to load
                await page.wait_for_timeout(1000) # Wait for a second before proceeding
                next_page_disabled = await next_page.get_attribute("disabled") # Check if "Next" button is disabled
                    
                if next_page_disabled is not None: # If "Next" button is disabled, exit loop
                    print(f"Next button disabled attribute: {next_page_disabled}")
                    print("Next button is disabled. Ending loop.")
                    break
                    
                print("Next button is endabled. Clicking next.")
                await next_page.click() 
                # Wait for the page to load after clicking
                await page.wait_for_load_state("networkidle")
                await page.wait_for_timeout(1000) # Wait for a second
                
    except TargetClosedError:
        print("The target page, context, or browser has been closed. Ending loop.")
        
    finally:
        if page is not None:
            await page.close()
        if browser is not None:
            await browser.close()
        
    # Output gathered data
    return laptops

# Path to lock file
lock_file_path = "/tmp/scraper.lock"

# main method
async def main():
    # Creating lock
    lock = InterProcessLock(lock_file_path)
    laptops = []
    if lock.acquire(blocking=False):
        try:
            # Run scraper code
            laptops = await run_scraper()
        finally:
            lock.release()
    else:
        print("Scraper is already running.")
        return
    return laptops


# initializing main method
if __name__ == "__main__":
    asyncio.run(main())
