# test_playwright.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://winmart.vn/")
    page.click('div.closeContainer')
    page.wait_for_timeout(5000)  # wait for JS to load, or use wait_for_selector
    # print(page.content())        # or page.locator('your-selector').all_text_contents()
    browser.close()
