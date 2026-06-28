class ConstraintService:

    @staticmethod
    def extract_constraints(text):

        constraints = {}

        text = text.lower()

        if "vegetarian" in text:
            constraints["catering_preference"] = "vegetarian"

        if "premium" in text:
            constraints["venue_preference"] = "premium"

        if "photography" in text:
            constraints["photography_priority"] = True

        return constraints