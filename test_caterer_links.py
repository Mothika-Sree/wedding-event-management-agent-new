from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-catering/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(10000)

    page.locator("div.vendor-card").first.wait_for()

    cards = page.locator("div.vendor-card")

    print("TOTAL CARDS:", cards.count())

    for i in range(min(10, cards.count())):

        try:

            href = cards.nth(i).locator(
                "a.vendor-detail"
            ).first.get_attribute("href")

            print(href)

        except Exception as e:

            print("ERROR:", e)

    input("ENTER")

    browser.close()