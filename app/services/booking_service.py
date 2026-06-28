from app.agents.booking_agent import BookingAgent
from app.services.profile_service import ProfileService
from app.services.memory_service import MemoryService

from playwright.sync_api import sync_playwright


class BookingService:

    @staticmethod
    async def prepare(package):

        profile = ProfileService.get_profile()
        preferences = MemoryService.get_preferences()

        booking_data = {
            "profile": profile,
            "preferences": preferences,
            "package": package
        }

        return await BookingAgent.prepare_booking(
            booking_data
        )

    @staticmethod
    def open_popup(page, vendor_type):

        try:

            if vendor_type == "venue":

                page.get_by_text(
                    "Check Availability & Prices"
                ).click(timeout=5000)

            else:

                page.get_by_text(
                    "Send Message"
                ).nth(1).click(timeout=5000)

            page.wait_for_timeout(1500)

            return True

        except Exception as e:

            print(f"{vendor_type}: Popup not found -> {e}")
            return False

    @staticmethod
    def fill_form(page, profile, package, vendor_type):

        # ------------------------
        # Name
        # ------------------------

        try:
            page.get_by_placeholder("Full name*").fill(profile["name"])
        except:
            try:
                page.locator('input[placeholder*="Full"]').first.fill(profile["name"])
            except:
                pass

        # ------------------------
        # Phone
        # ------------------------

        try:
            page.locator('input[name="contact"]').fill(profile["phone"])
        except:
            pass

        # ------------------------
        # Email
        # ------------------------

        try:
            page.get_by_placeholder("Email address").fill(profile["email"])
        except:
            try:
                page.locator('input[type="email"]').first.fill(profile["email"])
            except:
                pass

        # ------------------------
        # Guests (Venue/Caterer only)
        # ------------------------

        if vendor_type in ["venue", "caterer"]:

            try:
                page.get_by_placeholder(
                    "No of guests* (min 50)"
                ).fill(str(package["guest_count"]))
            except:
                pass

        # ------------------------
        # Wedding Details
        # ------------------------

        if vendor_type in ["decorator", "photographer"]:

            try:
                page.get_by_role(
                    "textbox",
                    name="Details about my wedding"
                ).fill(
                    f"We are planning a wedding for {package['guest_count']} guests.\n\n"
                    "Please share your pricing, availability and packages."
                )
            except:
                pass

        elif vendor_type == "caterer":

            try:
                page.get_by_placeholder(
                    "Details about my wedding"
                ).fill(
                    f"We are planning a wedding for {package['guest_count']} guests.\n\n"
                    "Please share your pricing, availability and packages."
                )
            except:
                pass

        print(f"{vendor_type} form filled.")

    @staticmethod
    def execute_browser_filling(package):

        profile = ProfileService.get_profile()

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            context = browser.new_context()

            vendors = [

                ("venue", package.get("venue_url")),

                ("caterer", package.get("caterer_url")),

                ("decorator", package.get("decorator_url")),

                ("photographer", package.get("photographer_url"))

            ]

            pages = []

            print("\nOpening vendor pages...\n")

            # -----------------------------------------
            # Open every vendor in a separate tab
            # -----------------------------------------

            for vendor_type, url in vendors:

                if not url:
                    continue

                page = context.new_page()

                page.goto(
                    url,
                    wait_until="networkidle"
                )

                pages.append(
                    (vendor_type, page)
                )

                print(f"{vendor_type} opened.")

            print("\nAll tabs opened.\n")

            # -----------------------------------------
            # Fill each tab
            # -----------------------------------------

            for vendor_type, page in pages:

                print(f"Processing {vendor_type}...")

                page.bring_to_front()

                if not BookingService.open_popup(
                    page,
                    vendor_type
                ):
                    continue

                BookingService.fill_form(
                    page,
                    profile,
                    package,
                    vendor_type
                )

                page.wait_for_timeout(1000)

            print("\n========================================")
            print("All enquiry forms have been filled.")
            print("Every vendor is open in a separate tab.")
            print("")
            print("Please review each tab.")
            print("Click 'Send Message' manually.")
            print("")
            print("When finished, return here.")
            print("========================================")

            input(
                "\nPress ENTER after submitting all enquiries..."
            )

            browser.close()

    @staticmethod
    async def confirm(session_id):

        return await BookingAgent.confirm_booking(
            session_id
        )