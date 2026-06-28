from playwright.sync_api import sync_playwright


class WedMeGoodDecoratorScraper:

    @staticmethod
    def get_decorators():

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = browser.new_page()

            page.goto(
                "https://www.wedmegood.com/vendors/chennai/wedding-decorators/",
                wait_until="networkidle"
            )

            page.wait_for_timeout(5000)
            print("TITLE:", page.title())
            print("URL:", page.url)
            page.screenshot(path="debug.png")

            cards = page.locator("div.vendor-card")

            print("TOTAL:", cards.count())
            vendor_links = []

            vendors = page.locator("a.vendor-detail")

            for i in range(vendors.count()):

                href = vendors.nth(i).get_attribute("href")

                if href:

                    vendor_links.append(
                        "https://www.wedmegood.com" + href
                    )

            print("TOTAL LINKS:", len(vendor_links))

            text = page.locator("#react-view").inner_text()

            browser.close()

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        decorators = []

        i = 0
        link_index = 0
        while i < len(lines):

            # Detect start of a decorator card
            if (
                i + 2 < len(lines)
                and (
                    (
                        lines[i + 1].replace(".", "", 1).isdigit()
                        and float(lines[i + 1]) <= 5.0
                    )
                    or lines[i + 1] == "No Reviews"
                )
            ):

                name = lines[i]

                # Skip unwanted entries
                if (
                    name.startswith("+")
                    or name == "Sponsored"
                    or name == "Featured"
                ):
                    i += 1
                    continue

                rating = lines[i + 1]
                reviews = lines[i + 2]

                location = ""
                starting_price = ""
                home_function_price = ""

                j = i + 3

                while j < len(lines):

                    line = lines[j]

                    # Stop if next decorator starts
                    if (
                        j + 2 < len(lines)
                        and (
                            (
                                lines[j + 1].replace(".", "", 1).isdigit()
                                and float(lines[j + 1]) <= 5.0
                            )
                            or lines[j + 1] == "No Reviews"
                        )
                    ):
                        break

                    # Stop when footer begins
                    if line.startswith("123456"):
                        break

                    if line in (
                        "Popular Searches",
                        "Latest Reviews",
                        "More Vendors in Chennai",
                        "Top Articles To Read",
                        "WedMeGood - Your Personal Wedding Planner",
                    ):
                        break

                    # Location
                    if (
                        "Chennai" in line
                        and not line.startswith("Wedding Decorators in")
                        and not line.startswith("Virtual Planning")
                        and not line.startswith("More Vendors")
                    ):
                        location = line

                    # Starting price
                    if line == "₹":
                        if j + 1 < len(lines):
                            starting_price = lines[j + 1].replace(",", "")

                    # Home function decor price
                    if line.startswith("Home function decor"):
                        home_function_price = (
                            line.replace("Home function decor", "")
                            .strip()
                            .replace(",", "")
                        )

                    j += 1

                vendor_url = ""

                if link_index < len(vendor_links):
                    vendor_url = vendor_links[link_index]
                    link_index += 1

                decorators.append(
                    {
                        "name": name,
                        "rating": rating,
                        "reviews": reviews,
                        "location": location,
                        "starting_price": starting_price,
                        "home_function_price": home_function_price,
                        "vendor_url": vendor_url
                    }
                )

                i = j

            else:
                i += 1

        return decorators


if __name__ == "__main__":
    decorators = WedMeGoodDecoratorScraper.get_decorators()

    from pprint import pprint
    pprint(decorators)

    print(f"\nTotal decorators: {len(decorators)}")
