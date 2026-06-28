from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://www.wedmegood.com/wedding-venues/Taj-Wellington-Mews-Chennai-2878203",
        wait_until="networkidle"
    )

    input(
        "\nOpen Send Message popup manually then press ENTER..."
    )

    # Full Name
    page.locator(
        'input[placeholder="Full name*"]'
    ).fill(
        "Mothika"
    )

    # Mobile Number
    page.locator(
        'input[name="contact"]'
    ).fill(
        "+919876543210"
    )

    # Email
    page.locator(
        'input[placeholder="Email address"]'
    ).fill(
        "mothika@gmail.com"
    )

    # Guests
    page.locator(
        'input[placeholder*="No of guests"]'
    ).fill(
        "300"
    )

    # Rooms
    page.locator(
        'input[placeholder="No of rooms"]'
    ).fill(
        "20"
    )

    # Wedding radio button
    page.locator(
        'input[type="radio"][value="Wedding"]'
    ).check(
        force=True
    )

    # Evening radio button
    page.locator(
        'input[type="radio"][value="Evening"]'
    ).check(
        force=True
    )

    print(
        "\nBasic venue details filled."
    )

    print(
        "\nFunction Date is still empty."
    )

    print(
        "\nClick the Function Date field manually and choose a date."
    )

    input(
        "\nAfter selecting date press ENTER..."
    )

    print(
        "\nVenue form filled successfully."
    )

    input(
        "\nVerify everything then press ENTER to close..."
    )

    browser.close()