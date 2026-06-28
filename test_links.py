from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-catering/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(5000)

    links = page.locator("a[href]")

    print("TOTAL LINKS:", links.count())

    for i in range(min(100, links.count())):

        href = links.nth(i).get_attribute("href")

        if href:
            print(href)

    input("ENTER")

    browser.close()