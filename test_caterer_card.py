from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-catering/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(10000)

    print("PAGE LOADED")

    print("TITLE:", page.title())

    print("URL:", page.url)

    print("\n--- HTML SAMPLE ---\n")

    html = page.content()

    print(html[:5000])

    with open(
        "caterer_html.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print("\nHTML SAVED")

    input("ENTER")

    browser.close()