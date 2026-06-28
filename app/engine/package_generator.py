from app.services.vendor_service import VendorService
from app.data.package_store import generated_packages
import uuid


class PackageGenerator:

    @staticmethod
    def calculate_package_cost(
        venue,
        caterer,
        decorator,
        photographer,
        guest_count
    ):

        veg_price = venue.get(
            "veg_price",
            0
        )

        rental_cost = venue.get(
            "rental_cost",
            0
        )

        if rental_cost > 0:
            venue_cost = rental_cost

        elif veg_price > 0:
            venue_cost = (
                veg_price * guest_count
            )

        else:
            return None

        caterer_price = caterer.get(
            "price",
            0
        )

        if caterer_price <= 0:
            return None

        catering_cost = (
            caterer_price * guest_count
        )

        decorator_cost = decorator.get(
            "price",
            0
        )

        if decorator_cost < 5000:
            return None

        photographer_cost = photographer.get(
            "price",
            0
        )

        if photographer_cost <= 0:
            return None

        total_cost = (
            venue_cost
            + catering_cost
            + decorator_cost
            + photographer_cost
        )

        return {
            "venue_cost": venue_cost,
            "catering_cost": catering_cost,
            "decorator_cost": decorator_cost,
            "photographer_cost": photographer_cost,
            "total_cost": total_cost
        }

    @staticmethod
    def generate_packages(
        location,
        guest_count,
        budget,
        preferences=None
    ):

        venues = VendorService.get_ranked_vendors(
            location,
            guest_count,
            budget,
            "venue",
            preferences
        )[:3]

        caterers = VendorService.get_ranked_vendors(
            location,
            guest_count,
            budget,
            "catering"
        )[:3]

        decorators = VendorService.get_ranked_vendors(
            location,
            guest_count,
            budget,
            "decoration"
        )[:3]

        photographers = VendorService.get_ranked_vendors(
            location,
            guest_count,
            budget,
            "photography"
        )[:3]

        packages = []

        for venue in venues:
            for caterer in caterers:
                for decorator in decorators:
                    for photographer in photographers:

                        costs = (
                            PackageGenerator.calculate_package_cost(
                                venue,
                                caterer,
                                decorator,
                                photographer,
                                guest_count
                            )
                        )

                        if costs is None:
                            continue

                        if costs["total_cost"] > budget:
                            continue

                        # Use at least 60% of budget
                        if costs["total_cost"] < budget * 0.5:
                            continue

                        average_score = (
                            venue.get("score", 0)
                            + caterer.get("score", 0)
                            + decorator.get("score", 0)
                            + photographer.get("score", 0)
                        ) / 4

                        # Minimum quality threshold
                        if average_score < 80:
                            continue

                        package = {

                            "package_id":
                            str(uuid.uuid4()),

                            "venue":
                            venue["name"],

                            "venue_url":
                            venue.get(
                                "vendor_url",
                                ""
                            ),

                            "caterer":
                            caterer["name"],

                            "caterer_url":
                            caterer.get(
                                "vendor_url",
                                ""
                            ),

                            "decorator":
                            decorator["name"],

                            "decorator_url":
                            decorator.get(
                                "vendor_url",
                                ""
                            ),

                            "photographer":
                            photographer["name"],

                            "photographer_url":
                            photographer.get(
                                "vendor_url",
                                ""
                            ),

                            "guest_count":
                            guest_count,

                            **costs,

                            "overall_score":
                            round(
                                average_score,
                                2
                            )
                        }

                        budget_gap = abs(budget - package["total_cost"])

                        budget_score = 100 - (budget_gap / budget) * 100

                        package["package_score"] = round(
                            package["overall_score"] * 0.7 +
                            budget_score * 0.3,
                            2
                        )

                        packages.append(
                            package
                        )

        packages.sort(
            key=lambda p: (
                p["package_score"],
                p["total_cost"]
            ),
            reverse=True
        )

        unique_packages = packages[:3]

        generated_packages.clear()

        for package in unique_packages:
            generated_packages[
                package["package_id"]
            ] = package

        return {
            "message":
            f"Found {len(unique_packages)} wedding packages",

            "location":
            location,

            "guest_count":
            guest_count,

            "budget":
            budget,

            "packages":
            unique_packages
        }