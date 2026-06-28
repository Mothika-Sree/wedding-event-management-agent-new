from playwright.sync_api import sync_playwright

class WedMeGoodAgent:

    @staticmethod
    def search_venues():

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(
                "https://www.wedmegood.com"
            )

            page.wait_for_timeout(5000)

            return {
                "status": "opened"
            }