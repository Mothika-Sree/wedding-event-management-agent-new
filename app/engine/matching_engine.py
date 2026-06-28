class MatchingEngine:

    @staticmethod
    def calculate_score(
        vendor,
        budget,
        guest_count,
    ):
        score = 0

        # ==========================
        # Safe values
        # ==========================

        budget = budget or 1
        guest_count = guest_count or 1

        rating = float(vendor.get("rating") or 0)
        price = float(vendor.get("price") or 0)

        capacity = vendor.get("capacity")
        if capacity is None:
            capacity = guest_count

        vendor_type = vendor.get("vendor_type", "")

        # ==========================
        # RATING SCORE (0–60)
        # ==========================

        score += rating * 12

        # ==========================
        # PRICE SCORE (0–30)
        # ==========================

        if vendor_type in ["venue", "catering"]:
            estimated_cost = price * guest_count
        else:
            estimated_cost = price

        if estimated_cost > 0:

            utilization = estimated_cost / budget

            price_score = max(
                0,
                30 - (utilization * 30)
            )

        else:

            price_score = 15

        score += price_score

        # ==========================
        # CAPACITY SCORE (0–10)
        # ==========================

        if capacity >= guest_count:

            extra_capacity = capacity - guest_count

            capacity_score = max(
                0,
                10 - ((extra_capacity / guest_count) * 5)
            )

        else:

            capacity_score = 0

        score += capacity_score

        return round(score, 2)

    @staticmethod
    def rank_vendors(
        vendors,
        budget,
        guest_count,
        preferences=None
    ):

        ranked = []

        for vendor in vendors:

            vendor_copy = vendor.copy()

            vendor_copy["score"] = MatchingEngine.calculate_score(
                vendor,
                budget,
                guest_count
            )

            ranked.append(vendor_copy)

        ranked.sort(
            key=lambda x: (
                x.get("score", 0),
                x.get("rating", 0)
            ),
            reverse=True
        )

        return ranked