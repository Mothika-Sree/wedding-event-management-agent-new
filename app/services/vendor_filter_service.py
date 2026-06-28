class VendorFilterService:

    @staticmethod
    def filter_vendors(
        vendors,
        location=None,
        budget=None,
        guest_count=None
    ):

        filtered = []

        for vendor in vendors:

            # Location filter
            if location:
                if location.lower() not in vendor.get(
                    "location", ""
                ).lower():
                    continue

            # Budget filter
            if budget:

                price = (
                    vendor.get("price")
                    or vendor.get("starting_price")
                    or "0"
                )

                try:
                    price = int(str(price).replace(",", ""))
                except:
                    price = 0

                if price > budget:
                    continue

            # Capacity filter
            if guest_count and "max_capacity" in vendor:

                cap = vendor["max_capacity"]

                digits = "".join(
                    c for c in cap if c.isdigit()
                )

                if digits:

                    if guest_count > int(digits):
                        continue

            filtered.append(vendor)

        return filtered