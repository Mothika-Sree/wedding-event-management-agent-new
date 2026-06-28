from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-venues/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(5000)

    card = page.locator("div.vendor-card").nth(1)

    print(card.inner_html())

    input("ENTER")

    browser.close()