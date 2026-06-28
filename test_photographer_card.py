from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-decorators/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(10000)

    html = page.content()

    with open(
        "decorator_html.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print("HTML SAVED")

    input("ENTER")

    browser.close()from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/vendors/chennai/wedding-photographers/",
        wait_until="networkidle"
    )

    page.wait_for_timeout(10000)

    html = page.content()

    with open(
        "photographer_html.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print("HTML SAVED")

    input("ENTER")

    browser.close()