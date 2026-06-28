import re
from playwright.sync_api import sync_playwright


class WedMeGoodVenueDetailScraper:

    @staticmethod
    def get_venue_details(url):

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded", timeout=120000)

            page.wait_for_timeout(5000)

            for _ in range(4):
                page.mouse.wheel(0, 5000)
                page.wait_for_timeout(1500)

            text = page.locator("body").inner_text()

            # Remove enquiry form section
            if "View Contact" in text and "Check Availability & Prices" in text:
                start = text.find("View Contact")
                end = text.find("Check Availability & Prices")

                if start != -1 and end != -1:
                    text = text[:start] + text[end:]

            lines = [
                line.strip()
                for line in text.split("\n")
                if line.strip()
            ]

            # --------------------------------
            # Name
            # --------------------------------

            name = ""

            for i, line in enumerate(lines):

                if line.startswith("Learn more"):

                    if i + 1 < len(lines):
                        name = lines[i + 1]

                    break

            # --------------------------------
            # Location
            # --------------------------------

            location = ""

            for i, line in enumerate(lines):

                if line == name:

                    if i + 1 < len(lines):
                        location = lines[i + 1]

                    break

            location = location.replace("(View on Map)", "").strip()

            # --------------------------------
            # Address
            # --------------------------------

            address = ""

            address_match = re.search(
                r'\(View on Map\)\s*(.*?)\s*5\.0',
                text,
                re.S
            )

            if address_match:

                address = " ".join(
                    address_match.group(1).split()
                )

            # --------------------------------
            # Rating
            # --------------------------------

            rating = ""

            match = re.search(r'(\d+\.\d)\s+\d+\s+reviews', text)

            if match:
                rating = match.group(1)

            # --------------------------------
            # Reviews Count
            # --------------------------------

            reviews_count = ""

            match = re.search(r'\d+\.\d\s+(\d+\s+reviews)', text)

            if match:
                reviews_count = match.group(1)

            # --------------------------------
            # Contact Number
            # --------------------------------

            contact_number = ""

            match = re.search(
                r'(\+91\s?\d{5}\s?\d{5})',
                text
            )

            if match:
                contact_number = match.group(1)

            # --------------------------------
            # Description
            # --------------------------------

            description = ""

            match = re.search(
                r'About .*?\n\n(.*?)\n\nSpace/Capacity',
                text,
                re.S
            )

            if match:

                description = " ".join(
                    match.group(1).split()
                )

            # --------------------------------
            # Rental Cost
            # --------------------------------

            rental_cost = ""

            match = re.search(
                r'₹\s*([\d,]+)\s*per function',
                text
            )

            if match:

                rental_cost = match.group(1).replace(",", "")

            # --------------------------------
            # Areas
            # --------------------------------

            areas = []

            area_matches = re.findall(
                r'(Indoor|Outdoor)\s+(\d+)\s+Seating\s+\|\s+(\d+)\s+Floating\s+(.*?)\n',
                text,
                re.S
            )

            for area_type, seating, floating, space in area_matches:

                areas.append({
                    "type": area_type,
                    "space": space.strip(),
                    "seating": seating,
                    "floating": floating
                })

            # --------------------------------
            # Facilities
            # --------------------------------

            facilities = []

            facilities_match = re.search(
                r'The facilities here include(.*?)Location of',
                text,
                re.S
            )

            if facilities_match:

                facilities = [
                    line.strip()
                    for line in facilities_match.group(1).split("\n")
                    if line.strip()
                ]

            # --------------------------------
            # Policies
            # --------------------------------

            policies = {}

            policy_labels = {
                "Catering policy": "catering",
                "Decor Policy": "decor",
                "Parking": "parking",
                "Outside Alcohol": "alcohol",
                "DJ Policy": "dj"
            }

            for label, key in policy_labels.items():

                match = re.search(
                    rf'{re.escape(label)}\s+(.*?)\n',
                    text
                )

                if match:
                    policies[key] = match.group(1).strip()

            # --------------------------------
            # Extra Information
            # --------------------------------

            experience = ""
            rooms = ""
            small_party = ""
            started_in = ""

            mappings = {
                "Been on WedMeGood Since": "experience",
                "Room Count": "rooms",
                "Small Party Venue": "small_party",
                "Start of Venue": "started_in"
            }

            extracted = {}

            for label, field in mappings.items():

                match = re.search(
                    rf'{re.escape(label)}\s+(.*?)\n',
                    text
                )

                if match:
                    extracted[field] = match.group(1).strip()

            experience = extracted.get("experience", "")
            rooms = extracted.get("rooms", "")
            small_party = extracted.get("small_party", "")
            started_in = extracted.get("started_in", "")

           # --------------------------------
            # Reviews
            # --------------------------------

            reviews = []

            try:
                review_start = next(
                    i for i, line in enumerate(lines)
                    if line.startswith("Reviews for")
                )

                faq_start = next(
                    i for i, line in enumerate(lines)
                    if line.startswith("FAQ about")
                )

                review_lines = lines[review_start:faq_start]

                i = 0

                while i < len(review_lines):

                    if (
                        review_lines[i].replace(".", "").isdigit()
                        and i + 2 < len(review_lines)
                        and review_lines[i + 1].startswith("Reviewed")
                    ):

                        rating = review_lines[i]

                        reviewer = review_lines[i - 1].strip()

                        reviewed_on = review_lines[i + 1]

                        comment_parts = []

                        j = i + 2

                        while j < len(review_lines):

                            line = review_lines[j]

                            # next review starts
                            if (
                                j + 2 < len(review_lines)
                                and review_lines[j + 1].replace(".", "").isdigit()
                                and review_lines[j + 2].startswith("Reviewed")
                            ):
                                break

                            # stop junk
                            if line in [
                                "Recommended for:",
                                "View All",
                                "Review Kailash Resort",
                                "Rate Vendor*",
                                "Add Photos",
                                "Submit Review"
                            ]:
                                j += 1
                                continue

                            comment_parts.append(line)

                            j += 1

                        comment = " ".join(comment_parts).strip()

                        reviews.append({
                            "reviewer": reviewer,
                            "rating": rating,
                            "reviewed_on": reviewed_on,
                            "comment": comment
                        })

                        i = j

                    else:
                        i += 1

            except:
                pass

            # --------------------------------
            # FAQs
            # --------------------------------

            faqs = []

            faq_matches = re.findall(
                r'([^\n?]+\?)\n(.*?)'
                r'(?=\n[^\n?]+\?|\nBrowse Similar)',
                text,
                re.S
            )

            for question, answer in faq_matches:

                faqs.append({
                    "question": question.strip(),
                    "answer": " ".join(answer.split())
                })

            # --------------------------------
            # Images
            # --------------------------------

            images = []

            vendor_id = url.rstrip("/").split("-")[-1]

            imgs = page.locator("img")

            for i in range(imgs.count()):

                src = imgs.nth(i).get_attribute("src")

                if not src:
                    continue

                if f"/uploads/member/{vendor_id}/" not in src:
                    continue

                src = re.sub(
                    r"/resized(?:-nw)?/\d+X/",
                    "/",
                    src
                )

                src = src.split("?")[0]

                if src not in images:
                    images.append(src)

            browser.close()

        return {
            "name": name,
            "location": location,
            "address": address,
            "rating": rating,
            "reviews_count": reviews_count,
            "contact_number": contact_number,
            "description": description,
            "rental_cost": rental_cost,
            "areas": areas,
            "facilities": facilities,
            "policies": policies,
            "experience": experience,
            "rooms": rooms,
            "small_party": small_party,
            "started_in": started_in,
            "faqs": faqs,
            "reviews": reviews,
            "images": images[:20],
            "vendor_url": url
        }