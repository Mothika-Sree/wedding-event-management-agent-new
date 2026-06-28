class VendorRankingService:

    @staticmethod
    def rank_vendors(
        vendors,
        budget=None,
        guest_count=None,
        location=None
    ):

        ranked = []

        for vendor in vendors:

            score = 0

            # Rating
            try:
                score += float(vendor.get("rating", 0)) * 20
            except:
                pass

            # Reviews
            reviews = vendor.get("reviews", "")
            digits = "".join(c for c in reviews if c.isdigit())

            if digits:
                score += min(int(digits), 200) * 0.2

            # Budget
            price = (
                vendor.get("starting_price")
                or vendor.get("price")
                or "0"
            )

            try:
                price = int(str(price).replace(",", ""))
            except:
                price = 0

            if budget:

                if price <= budget:
                    score += 30
                else:
                    score -= 10

            # Guest Capacity (Venue/Caterer)
            if guest_count:

                capacity = vendor.get("capacity") or vendor.get("max_capacity")

                if capacity:

                    digits = "".join(
                        c for c in str(capacity)
                        if c.isdigit()
                    )

                    if digits and int(digits) >= guest_count:
                        score += 20

            # Location
            if (
                location
                and location.lower()
                in vendor.get("location", "").lower()
            ):
                score += 15

            vendor["score"] = round(score, 2)

            ranked.append(vendor)

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked