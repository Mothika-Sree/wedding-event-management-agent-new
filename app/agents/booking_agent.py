from app.data.booking_db import (
    save_booking
)

from app.services.profile_service import (
    ProfileService
)
from playwright.async_api import async_playwright

from app.data.booking_store import (
    booking_sessions
)
from app.services.profile_service import ProfileService

profile = ProfileService.get_profile()

class BookingAgent:
    @staticmethod
    async def prepare_booking(data):

        profile = data["profile"]
        package = data["package"]
        preferences = data["preferences"]
        print(data)
        booking_data = {

            "customer_name":
                profile.get("name", ""),

            "customer_email":
                profile.get("email", ""),

            "customer_phone":
                profile.get("phone", ""),

            "venue":
                package.get("venue", ""),

            "caterer":
                package.get("caterer", ""),

            "decorator":
                package.get("decorator", ""),

            "photographer":
                package.get("photographer", ""),

            "guest_count":
                preferences.get("guest_count", 100),

            "budget":
                preferences.get("budget", ""),

            "event_type":
                preferences.get("event_type", ""),

            "special_requests":
                ""
        }

        booking_sessions[
            package["package_id"]
        ] = booking_data

        return {
            "session_id":
                package["package_id"],

            "booking_data":
                booking_data,

            "message":
                "Booking form prepared"
        }