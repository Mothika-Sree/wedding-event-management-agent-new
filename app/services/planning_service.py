import re
from app.services.memory_service import MemoryService


class PlanningService:

    @staticmethod
    def parse_request(text):

        text_lower = text.lower()

        # -----------------
        # LOCATION
        # -----------------

        location = "Chennai"

        cities = [
            "chennai",
            "coimbatore",
            "madurai",
            "bangalore",
            "hyderabad"
        ]

        for city in cities:
            if city in text_lower:
                location = city.title()
                break

        # -----------------
        # GUEST COUNT
        # -----------------

        guest_match = re.search(
            r"(\d+)\s*(guests?|people|attendees?)",
            text_lower
        )

        guest_count = (
            int(guest_match.group(1))
            if guest_match
            else 100
        )

        # -----------------
        # BUDGET
        # -----------------

        budget = 200000

        lakh_match = re.search(
            r"(\d+)\s*(lakh|lakhs)",
            text_lower
        )

        if lakh_match:
            budget = int(
                lakh_match.group(1)
            ) * 100000

        else:

            budget_match = re.search(
                r"(budget|under)\s*₹?\s*(\d+)",
                text_lower
            )

            if budget_match:
                budget = int(
                    budget_match.group(2)
                )

        # -----------------
        # EVENT TYPE
        # -----------------

        event_type = "Wedding"

        if "birthday" in text_lower:
            event_type = "Birthday"

        elif "corporate" in text_lower:
            event_type = "Corporate"

        elif "engagement" in text_lower:
            event_type = "Engagement"

        elif "conference" in text_lower:
            event_type = "Conference"

        # -----------------
        # PREFERENCES
        # -----------------

        preferences = MemoryService.get_preferences()

        return {
            "location": location,
            "guest_count": guest_count,
            "budget": budget,
            "event_type": event_type,
            "preferences": preferences
        }