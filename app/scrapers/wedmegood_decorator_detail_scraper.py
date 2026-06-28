from playwright.sync_api import sync_playwright
import re

class WedMeGoodDecoratorDetailScraper:

    @staticmethod
    def get_decorator_details(vendor_url: str):
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
            if "Starting Price" in line or "Pricing Info" in line:
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j] == "₹" and j + 1 < len(lines):
                        starting_price = lines[j+1].replace(",", "")
                        break
                if starting_price:
                    break

        # ------------------------------------
        # DECOR STYLES
        # ------------------------------------
        decor_styles = []
        for i, line in enumerate(lines):
            if "Services provided by" in line:
                for j in range(i + 1, min(i + 20, len(lines))):
                    if "Key cities" in lines[j] or "Specialisation" in lines[j] or lines[j].endswith("?"):
                        break
                    decor_styles.append(lines[j])
                break
        decor_styles = [s for s in decor_styles if len(s) < 50 and not s.startswith("They ") and not s.startswith("We ")]

        # ------------------------------------
        # OUTDOOR EVENTS
        # ------------------------------------
        outdoor_events = ""
        for i, line in enumerate(lines):
            if "Outdoor Budget" in line:
                price_str = ""
                for j in range(max(0, i-5), min(len(lines), i+5)):
                    if lines[j] == "₹" and j + 1 < len(lines):
                        price_str = lines[j+1]
                outdoor_events = f"Yes, outdoor decor available (Budget: {price_str})" if price_str else "Yes, outdoor decor available"
                break
        if not outdoor_events:
            outdoor_events = "Information not available"

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
            "decor_styles": decor_styles,
            "outdoor_events": outdoor_events,
            "experience": experience,
            "images": images[:20],
            "reviews": reviews[:10],
            "faqs": faqs
        }
