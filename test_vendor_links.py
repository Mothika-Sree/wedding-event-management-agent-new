# test_vendor_links.py

from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-catering/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(5000)

    vendors = page.locator("a.vendor-detail")

    print("TOTAL:", vendors.count())

    for i in range(vendors.count()):

        href = vendors.nth(i).get_attribute("href")

        print(i, href)

    input("ENTER")