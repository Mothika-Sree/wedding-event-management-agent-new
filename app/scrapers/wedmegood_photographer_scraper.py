# app/scrapers/wedmegood_photographer_scraper.py

from playwright.async_api import async_playwright


class WedMeGoodPhotographerScraper:

    @staticmethod
    def get_photographers():

        photographers = []

        with async_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            try:

                page.goto(
                    "https://www.wedmegood.com/vendors/chennai/wedding-photographers/",
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(10000)

            except Exception as e:

                print(
                    "PHOTOGRAPHER SCRAPER ERROR:",
                    str(e)
                )

                browser.close()
                return []

            vendor_links = []

            vendors = page.locator(
                "a.vendor-detail"
            )

            for i in range(vendors.count()):

                href = vendors.nth(i).get_attribute(
                    "href"
                )

                if href:

                    vendor_links.append(
                        "https://www.wedmegood.com" + href
                    )

            print(
                "TOTAL LINKS:",
                len(vendor_links)
            )

            try:

                text = page.locator(
                    "#react-view"
                ).inner_text()

            except Exception as e:

                print(
                    "TEXT EXTRACTION ERROR:",
                    str(e)
                )

                browser.close()
                return []

            browser.close()

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        link_index = 0
        i = 0

        while i < len(lines):

            line = lines[i].strip()

            try:

                if (
                    i + 2 < len(lines)
                    and lines[i + 1]
                    .strip()
                    .replace(".", "", 1)
                    .isdigit()
                    and "review"
                    in lines[i + 2].lower()
                ):

                    name = line

                    rating = lines[i + 1].strip()

                    reviews = lines[i + 2].strip()

                    city = ""
                    service = ""
                    price = ""

                    for j in range(
                        i + 3,
                        min(i + 20, len(lines))
                    ):

                        value = lines[j].strip()

                        if (
                            "Chennai" in value
                            and len(value) < 50
                        ):
                            city = value

                        elif (
                            "Photo" in value
                            or "Photography" in value
                        ):
                            service = value

                        elif (
                            value.replace(",", "")
                            .isdigit()
                        ):
                            price = value

                    vendor_url = ""

                    if (
                        link_index
                        < len(vendor_links)
                    ):

                        vendor_url = (
                            vendor_links[
                                link_index
                            ]
                        )

                        link_index += 1

                    photographers.append(
                        {
                            "name": name,
                            "rating": rating,
                            "reviews": reviews,
                            "city": city,
                            "service": service,
                            "price": price,
                            "vendor_url": vendor_url
                        }
                    )

                    i += 10
                    continue

            except Exception as e:

                print(
                    "PARSE ERROR:",
                    str(e)
                )

            i += 1

        print(
            "TOTAL PHOTOGRAPHERS PARSED:",
            len(photographers)
        )

        if photographers:

            print(
                "\nFIRST PHOTOGRAPHER:"
            )

            print(
                photographers[0]
            )

        return photographers[:20]


if __name__ == "__main__":

    result = (
        WedMeGoodPhotographerScraper
        .get_photographers()
    )

    print("\nRESULT COUNT:")
    print(len(result))
