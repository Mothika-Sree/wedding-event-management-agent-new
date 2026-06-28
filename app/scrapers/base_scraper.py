from playwright.sync_api import sync_playwright


class BaseScraper:

    @staticmethod
    def get_page(url):

        p = sync_playwright().start()

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(url, wait_until="networkidle")

        page.wait_for_timeout(5000)

        return p, browser, page