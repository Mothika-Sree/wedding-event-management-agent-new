from playwright.sync_api import sync_playwright

class WedMeGoodCatererScraper:

    @staticmethod
    def get_caterers():

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto(
                "https://www.wedmegood.com/vendors/chennai/wedding-catering/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(5000)
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
            with open("caterer_page.txt", "w", encoding="utf-8") as f:
                            f.write(text)

            browser.close()

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        caterers = []

        i = 0
        link_index = 0

        while i < len(lines):

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

                rating = lines[i + 1]

                reviews = ""
                location = ""
                price = ""
                max_capacity = ""
                min_capacity = ""

                j = i + 2

                if "review" in lines[j].lower():
                    reviews = lines[j]
                    j += 1

                while j < min(i + 20, len(lines)):

                    value = lines[j]

                    if (
                        value.startswith("How")
                        or value.startswith("The ability")
                        or value.startswith("Things to")
                        or value.startswith("Wedding Catering")
                        or value.startswith("Frequently Asked Questions")
                    ):
                        break

                    if (
                        "Chennai" in value
                        and len(value) < 60
                    ):
                        location = value

                    if value == "₹" and j + 1 < len(lines):
                        price = lines[j + 1]

                    if value.startswith("Max"):
                        max_capacity = value

                    if value.startswith("Min"):
                        min_capacity = value

                    j += 1

                vendor_url = ""

                if link_index < len(vendor_links):
                    vendor_url = vendor_links[link_index]
                    link_index += 1

                caterers.append(
                    {
                        "name": name,
                        "rating": rating,
                        "reviews": reviews,
                        "location": location,
                        "price": price,
                        "max_capacity": max_capacity,
                        "min_capacity": min_capacity,
                        "vendor_url": vendor_url
                    }
                )

                i += 2
                continue

            i += 1

        return caterers


if __name__ == "__main__":

    caterers = WedMeGoodCatererScraper.get_caterers()

    from pprint import pprint

    pprint(caterers)

    print("\nTOTAL:", len(caterers))