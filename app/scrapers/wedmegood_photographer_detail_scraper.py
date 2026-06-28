from playwright.sync_api import sync_playwright
import re

class WedMeGoodPhotographerDetailScraper:

    @staticmethod
    def get_photographer_details(vendor_url: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(vendor_url, wait_until="networkidle")
            page.wait_for_timeout(5000)
            text = page.locator("#react-view").inner_text()
            
            # Extract images
            images = []
            vendor_id = ""
            match = re.search(r'-(\d+)$', vendor_url)
            if match:
                vendor_id = match.group(1)
            for img in page.locator("img").evaluate_all("els => els.map(e => e.src)"):
                if img and "uploads/member" in img and f"/{vendor_id}/" in img and img not in images:
                    images.append(img)
                    if len(images) >= 15:
                        break
            browser.close()

        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # ------------------------------------
        # DESCRIPTION
        # ------------------------------------
        description = ""
        for i, line in enumerate(lines):
            if line.startswith("About ") and " - " in line:
                desc_lines = []
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if (next_line.startswith("Been on WedMeGood Since") or 
                        next_line.startswith("Reviews for") or 
                        next_line.startswith("About the team") or 
                        next_line.startswith("Services provided") or 
                        next_line.startswith("Services Offered") or
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
        # STARTING PRICE
        # ------------------------------------
        starting_price = ""
        for i, line in enumerate(lines):
            if "Per Day Price Estimate" in line or "Pricing Info" in line:
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j] == "₹" and j + 1 < len(lines):
                        starting_price = lines[j+1].replace(",", "")
                        break
                if starting_price:
                    break

        # ------------------------------------
        # SERVICES
        # ------------------------------------
        services = []
        for i, line in enumerate(lines):
            if "Services Offered" in line:
                for j in range(i + 1, min(i + 15, len(lines))):
                    if "Been on" in lines[j] or "Payment" in lines[j] or lines[j].endswith("?"):
                        break
                    services.append(lines[j])
                break

        # ------------------------------------
        # TRAVEL POLICY
        # ------------------------------------
        travel_policy = ""
        for i, line in enumerate(lines):
            if "Travel Cost" in line or "Travel Policy" in line:
                if i + 1 < len(lines):
                    travel_policy = lines[i + 1]
                    break

        # ------------------------------------
        # DELIVERY TIME
        # ------------------------------------
        delivery_time = ""
        for i, line in enumerate(lines):
            if "Delivery Time" in line or "Delivery time" in line:
                if i + 1 < len(lines):
                    delivery_time = lines[i + 1]
                    break
            if "Delivery time:" in line:
                delivery_time = line
                break

        # ------------------------------------
        # EXPERIENCE
        # ------------------------------------
        experience = ""
        for i, line in enumerate(lines):
            if "Been on WedMeGood Since" in line and i + 1 < len(lines):
                experience = lines[i + 1]
                break

        # ------------------------------------
        # FAQS & REVIEWS
        # ------------------------------------
        faqs = []
        for i in range(len(lines)):
            question = lines[i]
            if question.endswith("?") and i + 1 < len(lines):
                faqs.append({
                    "question": question,
                    "answer": lines[i + 1]
                })

        reviews = []
        for i in range(len(lines)):
            if re.match(r"^\d\.\d$", lines[i]) and i >= 1 and i + 2 < len(lines) and "Reviewed" in lines[i + 1]:
                reviews.append({
                    "reviewer": lines[i - 1],
                    "rating": lines[i],
                    "comment": lines[i + 2]
                })

        return {
            "vendor_url": vendor_url,
            "description": description,
            "starting_price": starting_price,
            "services": services,
            "travel_policy": travel_policy,
            "delivery_time": delivery_time,
            "experience": experience,
            "images": images[:20],
            "reviews": reviews[:10],
            "faqs": faqs
        }
