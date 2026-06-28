from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/wedding-venues/Taj-Wellington-Mews-Chennai-2878203",
        wait_until="networkidle"
    )

    input(
        "\nOpen the Send Message popup manually, then press ENTER..."
    )

    try:
        print(
            page.locator("form").first.evaluate(
                "form => form.outerHTML"
            )
        )
    except Exception as e:
        print("ERROR:", e)

    input("\nPress ENTER to close...")

    browser.close()