from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page(viewport={"width": 1400, "height": 900})

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-venues/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(5000)

    name = page.locator("a.vendor-detail").first

    # Go to the parent container (vendor card)
    card = name.locator("xpath=ancestor::*[contains(@class,'vendor')][1]")

    print(card.inner_html())

    browser.close()