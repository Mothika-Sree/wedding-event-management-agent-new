from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-catering/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(10000)

    links = page.locator("a")

    print("TOTAL A TAGS:", links.count())

    for i in range(min(100, links.count())):

        href = links.nth(i).get_attribute("href")

        if href and "/profile/" in href:

            print(href)

    input("ENTER")