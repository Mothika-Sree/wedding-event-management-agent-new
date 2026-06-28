from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/profile/Party-Planners-Caterers-1443384"
    )

    input("Open the Send Message popup manually, then press ENTER...")

    page.locator(
        'input[placeholder="Full name*"]'
    ).fill("Test User")

    page.locator(
        'input[placeholder="Mobile number*"]'
    ).fill("9876543210")

    page.locator(
        'input[placeholder="Email address"]'
    ).fill("test@gmail.com")

    page.locator(
        'input[placeholder="Details about my wedding"]'
    ).fill(
        "Need catering for wedding reception."
    )

    print("FILLED SUCCESSFULLY")

    input("Press ENTER to close")

    browser.close()