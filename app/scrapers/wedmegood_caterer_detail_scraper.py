from playwright.sync_api import sync_playwright
import re


class WedMeGoodCatererDetailScraper:

    @staticmethod
    def get_caterer_details(vendor_url: str):

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto(
                vendor_url,
                wait_until="networkidle"
            )

            page.wait_for_timeout(5000)

            text = page.locator("#react-view").inner_text()

            # Extract images
            import re

            images = []

            vendor_id = ""

            match = re.search(r'-(\d+)$', vendor_url)

            if match:
                vendor_id = match.group(1)

            for img in page.locator("img").evaluate_all(
                "els => els.map(e => e.src)"
            ):

                if (
                    img
                    and "uploads/member" in img
                    and f"/{vendor_id}/" in img
                    and img not in images
                ):
                    images.append(img)

                    if len(images) >= 15:
                        break
            browser.close()

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        description = ""

        veg_price = ""
        nonveg_price = ""

        max_capacity = ""
        min_capacity = ""

        reviews = []

        faqs = []

        # ------------------------------------
        # DESCRIPTION
        # ------------------------------------
        description = ""
        found_about = False
        for i, line in enumerate(lines):
            if line.startswith("About ") and " - " in line:
                found_about = True
                desc_lines = []
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if (next_line.startswith("Been on WedMeGood Since") or 
                        next_line.startswith("Reviews for") or 
                        next_line.startswith("About the team") or 
                        next_line.startswith("Services provided") or 
                        next_line.startswith("Specialisation") or 
                        next_line.startswith("FAQ about") or 
                        next_line.startswith("Payment terms") or 
                        next_line.startswith("Travel Cost") or 
                        next_line.startswith("Year of operations") or 
                        next_line.startswith("Experience Zones")):
                        break
                    if len(next_line) < 80 and ("chennai" in next_line.lower() or next_line.strip() == "" or len(next_line) < 20):
                        continue
                    desc_lines.append(next_line)
                description = " ".join(desc_lines).strip()
                break

        # ------------------------------------
        # CUISINES
        # ------------------------------------
        cuisines = []
        cuisines_str = ""
        cuisines_match = re.search(r"Cuisines offered:\s*(.*)", description, re.IGNORECASE)
        if cuisines_match:
            cuisines_str = cuisines_match.group(1)
        else:
            for line in lines:
                if "Cuisines offered" in line:
                    parts = line.split("Cuisines offered:")
                    if len(parts) > 1:
                        cuisines_str = parts[1]
                        break
        if cuisines_str:
            known = ["North Indian", "South Indian", "Chinese", "Desserts", "Italian", "Continental", "Thai", "Mexican", "Mughlai", "Chettinad", "Jain", "Chaat", "Street Food"]
            for c in known:
                if c.lower() in cuisines_str.lower():
                    cuisines.append(c)
            if not cuisines:
                cuisines = [x.strip() for x in re.split(r'[,&]|\s{2,}', cuisines_str) if x.strip()]

        # ------------------------------------
        # EXPERIENCE
        # ------------------------------------
        experience = ""
        for i, line in enumerate(lines):
            if "Been on WedMeGood Since" in line and i + 1 < len(lines):
                experience = lines[i + 1]
                break

        # ------------------------------------
        # SPECIALITIES
        # ------------------------------------
        specialities = []
        for i, line in enumerate(lines):
            if "Specialisation of" in line and i + 1 < len(lines):
                specialities.append(lines[i + 1])
        if not specialities:
            for spec in ["Full Service Catering", "Food Counters", "Small Function Catering"]:
                if spec.lower() in description.lower():
                    specialities.append(spec + " Specialist")

        # ------------------------------------
        # POLICIES
        # ------------------------------------
        policies_list = []
        for i, line in enumerate(lines):
            if "Payment terms" in line or "Cancellation policy" in line or "Booking policy" in line:
                if i + 1 < len(lines):
                    policies_list.append(f"{line}: {lines[i+1]}")
        policies = "; ".join(policies_list) if policies_list else "Information not available"

        # ------------------------------------
        # FAQS
        # ------------------------------------

        for i in range(len(lines)):

            question = lines[i]

            if (
                question.endswith("?")
                and i + 1 < len(lines)
            ):

                answer = lines[i + 1]

                faqs.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

                # Veg Price
                if (
                    "vegetarian menu" in question.lower()
                    and not veg_price
                ):

                    match = re.search(r"(\d+)", answer)

                    if match:
                        veg_price = match.group(1)

                # Non Veg Price
                if (
                    "non-vegetarian menu" in question.lower()
                    and not nonveg_price
                ):

                    match = re.search(r"(\d+)", answer)

                    if match:
                        nonveg_price = match.group(1)

        # ------------------------------------
        # CAPACITY
        # ------------------------------------

        for i in range(len(lines)):

            if lines[i] == "Max Capacity":

                if i + 1 < len(lines):

                    match = re.search(
                        r"(\d+)",
                        lines[i + 1]
                    )

                    if match:

                        max_capacity = match.group(1)

            if lines[i] == "Min Capacity":

                if i + 1 < len(lines):

                    match = re.search(
                        r"(\d+)",
                        lines[i + 1]
                    )

                    if match:

                        min_capacity = match.group(1)

        # ------------------------------------
        # REVIEWS
        # ------------------------------------

        for i in range(len(lines)):

            if (
                re.match(r"^\d\.\d$", lines[i])
                and i >= 1
                and i + 2 < len(lines)
                and "Reviewed" in lines[i + 1]
            ):

                reviewer = lines[i - 1]

                rating = lines[i]

                comment = lines[i + 2]

                reviews.append(
                    {
                        "reviewer": reviewer,
                        "rating": rating,
                        "comment": comment
                    }
                )

        return {
            "vendor_url": vendor_url,
            "description": description,
            "veg_price": veg_price,
            "nonveg_price": nonveg_price,
            "max_capacity": max_capacity,
            "min_capacity": min_capacity,
            "reviews": reviews[:10],
            "faqs": faqs,
            "images": images[:20],
            "specialities": specialities,
            "cuisines": cuisines,
            "experience": experience,
            "policies": policies
        }