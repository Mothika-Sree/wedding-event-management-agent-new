from app.engine.matching_engine import MatchingEngine

from app.services.wedmegood_service import (
    WedMeGoodService
)

from app.services.wedmegood_caterer_service import (
    WedMeGoodCatererService
)

from app.services.wedmegood_decorator_service import (
    WedMeGoodDecoratorService
)

from app.services.wedmegood_photographer_service import (
    WedMeGoodPhotographerService
)

_vendor_cache = []


def safe_rating(value):
    try:
        return float(value)
    except:
        return 0.0


def safe_price(value):
    try:
        return int(
            str(value)
            .replace(",", "")
            .replace("₹", "")
            .strip()
        )
    except:
        return 0


class VendorService:

    @staticmethod
    def get_all_vendors():

        global _vendor_cache

        if _vendor_cache:
            return _vendor_cache

        vendors = []

        # ==========================
        # VENUES
        # ==========================

        try:
            venues = WedMeGoodService.get_venues()

            for venue in venues:

                veg_price = safe_price(
                    venue.get("veg_price", 0)
                )

                rental_cost = safe_price(
                    venue.get("rental_cost", 0)
                )

                price = 0

                if veg_price > 0:
                    price = veg_price

                elif rental_cost > 0:
                    price = rental_cost

                vendors.append(
                    {
                        "name": venue["name"],
                        "vendor_type": "venue",
                        "location": venue.get(
                            "location",
                            "Chennai"
                        ),

                        "price": price,

                        "veg_price": veg_price,
                        "rental_cost": rental_cost,

                        "capacity": 1000,

                        "rating": safe_rating(
                            venue.get("rating", 0)
                        ),

                        "available": True,

                        "vendor_url": venue.get(
                            "vendor_url",
                            ""
                        )
                    }
                )

            print("VENUES LOADED:", len(venues))

        except Exception as e:
            print("VENUE ERROR:", e)

        # ==========================
        # CATERERS
        # ==========================

        try:

            caterers = (
                WedMeGoodCatererService
                .get_caterers()
            )

            for caterer in caterers:

                price = safe_price(
                    caterer.get("price")
                    or caterer.get("starting_price")
                    or 0
                )

                vendors.append(
                    {
                        "name": caterer["name"],
                        "vendor_type": "catering",
                        "location": caterer.get(
                            "location",
                            "Chennai"
                        ),
                        "price": price,
                        "capacity": 1000,
                        "rating": safe_rating(
                            caterer.get("rating", 0)
                        ),
                        "available": True,
                        "vendor_url": caterer.get(
                            "vendor_url",
                            ""
                        )
                    }
                )

            print(
                "CATERERS LOADED:",
                len(caterers)
            )

        except Exception as e:
            print("CATERER ERROR:", e)

        # ==========================
        # DECORATORS
        # ==========================

        try:

            decorators = (
                WedMeGoodDecoratorService
                .get_decorators()
            )

            for decorator in decorators:

                price = safe_price(
                    decorator.get("price")
                    or decorator.get(
                        "starting_price"
                    )
                    or 0
                )

                vendors.append(
                    {
                        "name": decorator["name"],
                        "vendor_type": "decoration",
                        "location": decorator.get(
                            "location",
                            "Chennai"
                        ),
                        "price": price,
                        "capacity": 1000,
                        "rating": safe_rating(
                            decorator.get("rating", 0)
                        ),
                        "available": True,
                        "vendor_url": decorator.get(
                            "vendor_url",
                            ""
                        )
                    }
                )

            print(
                "DECORATORS LOADED:",
                len(decorators)
            )

        except Exception as e:
            print("DECORATOR ERROR:", e)

        # ==========================
        # PHOTOGRAPHERS
        # ==========================

        try:

            photographers = (
                WedMeGoodPhotographerService
                .get_photographers()
            )

            for photographer in photographers:

                price = safe_price(
                    photographer.get("price")
                    or photographer.get(
                        "starting_price"
                    )
                    or 0
                )

                vendors.append(
                    {
                        "name": photographer["name"],
                        "vendor_type": "photography",
                        "location": photographer.get(
                            "city",
                            photographer.get(
                                "location",
                                "Chennai"
                            )
                        ),
                        "price": price,
                        "capacity": 1000,
                        "rating": safe_rating(
                            photographer.get("rating", 0)
                        ),
                        "available": True,
                        "vendor_url": photographer.get(
                            "vendor_url",
                            ""
                        )
                    }
                )

            print(
                "PHOTOGRAPHERS LOADED:",
                len(photographers)
            )

        except Exception as e:
            print(
                "PHOTOGRAPHER ERROR:",
                e
            )

        _vendor_cache.extend(vendors)

        print(
            "TOTAL VENDORS:",
            len(_vendor_cache)
        )

        return _vendor_cache

    @staticmethod
    def filter_vendors(
            location,
            guest_count,
            budget,
            vendor_type
        ):

            vendors = VendorService.get_all_vendors()

            filtered = []

            vendor_types = [
                v.strip().lower()
                for v in vendor_type.split(",")
            ]

            for vendor in vendors:

                # -------------------------
                # Available
                # -------------------------
                if not vendor.get("available", False):
                    continue

                # -------------------------
                # Vendor type
                # -------------------------
                if vendor.get("vendor_type", "").lower() not in vendor_types:
                    continue

                # -------------------------
                # Location
                # -------------------------
                vendor_location = str(
                    vendor.get("location") or ""
                ).lower()

                if location.lower() not in vendor_location:
                    continue

                # -------------------------
                # Capacity
                # -------------------------
                capacity = vendor.get("capacity")

                if capacity is None:
                    capacity = guest_count

                if (
                    guest_count is not None
                    and capacity < guest_count
                ):
                    continue

                filtered.append(vendor)

            return filtered


    @staticmethod
    def get_ranked_vendors(
            location,
            guest_count,
            budget,
            vendor_type,
            preferences = None
        ):

            filtered = VendorService.filter_vendors(
                location,
                guest_count,
                budget,
                vendor_type
            )

            return MatchingEngine.rank_vendors(
                filtered,
                budget,
                guest_count,
            )