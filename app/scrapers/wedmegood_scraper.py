from playwright.sync_api import sync_playwright

class WedMeGoodScraper:

    @staticmethod
    def get_venues():

        venues = []
        
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1366, "height": 768},
                locale="en-US",
                timezone_id="Asia/Kolkata"
            )

            page = context.new_page()

            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1"
            })

            page.goto(
                "https://www.wedmegood.com/vendors/chennai/wedding-venues/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(8000)

            print("TITLE:", page.title())
            print("URL:", page.url)

            page.screenshot(path="/tmp/debug.png", full_page=True)

            print("HTML START:")
            print(page.content()[:1000])

            cards = page.locator("div.vendor-card")

            print("TOTAL:", cards.count())
            for i in range(1, cards.count(), 2):

                try:

                    card = cards.nth(i)

                    name = (
                        card.locator("a.vendor-detail")
                        .first
                        .inner_text()
                        .strip()
                    )

                    vendor_url = (
                        "https://www.wedmegood.com"
                        + card.locator(
                            "a.vendor-detail"
                        ).first.get_attribute("href")
                    )

                    rating = (
                        card.locator(
                            "span.StarRatingNew"
                        ).inner_text()
                        .strip()
                    )

                    reviews = (
                        card.locator(
                            "span.review-cnt"
                        ).inner_text()
                        .strip()
                    )

                    info_blocks = card.locator(
                        "div.info-icon.text-tertiary"
                    )

                    location = ""

                    venue_type = ""

                    if info_blocks.count() > 0:
                        location = (
                            info_blocks
                            .nth(0)
                            .inner_text()
                            .strip()
                        )

                    if info_blocks.count() > 1:
                        venue_type = (
                            info_blocks
                            .nth(1)
                            .inner_text()
                            .strip()
                        )

                    card_text = card.inner_text()

                    veg_price = ""
                    nonveg_price = ""
                    rental_cost = ""
                    pricing_type = ""

                    lines = [
                        x.strip()
                        for x in card_text.split("\n")
                        if x.strip()
                    ]

                    for idx, line in enumerate(lines):

                        if (
                            line == "Veg"
                            and idx + 2 < len(lines)
                        ):
                            veg_price = lines[idx + 2]

                        if (
                            line == "Non veg"
                            and idx + 2 < len(lines)
                        ):
                            nonveg_price = lines[idx + 2]

                        if line == "Rental cost":
                            pricing_type = "Rental Cost"

                        if line == "Rental Only":
                            pricing_type = "Rental Only"

                        if line == "Price on Request":
                            pricing_type = "Price on Request"

                    venues.append(
                        {
                            "name": name,
                            "rating": rating,
                            "reviews": reviews,
                            "location": location,
                            "venue_type": venue_type,
                            "veg_price": veg_price,
                            "nonveg_price": nonveg_price,
                            "rental_cost": rental_cost,
                            "pricing_type": pricing_type,
                            "vendor_url": vendor_url
                        }
                    )

                except Exception as e:

                    print("SKIPPED:", e)

            browser.close()

        return venues[:20]
