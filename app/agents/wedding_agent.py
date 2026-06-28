# app/agents/wedding_agent.py

import re

from app.engine.package_generator import PackageGenerator

from app.data.package_store import (
    generated_packages,
    approved_packages
)

from app.services.form_service import FormService
from app.services.booking_service import BookingService


class WeddingAgent:

    def extract_details(self, message: str):

        location = None
        budget = None
        guest_count = None
        budget_match = re.search(
            r'(\d+)\s*(lakh|lakhs)',
            message.lower()
        )

        if budget_match:
            budget = (
                int(budget_match.group(1))
                * 100000
            )

        guest_match = re.search(
            r'(\d+)\s*(guest|guests|people)',
            message.lower()
        )

        if guest_match:
            guest_count = int(
                guest_match.group(1)
            )
        cities = [
            "chennai",
            "bangalore",
            "hyderabad",
            "mumbai",
            "delhi"
        ]

        for city in cities:

            if city in message.lower():

                location = city.title()
                break

        return {
            "location": location,
            "budget": budget,
            "guest_count": guest_count,
        }

    def process(self, message: str):

        msg = message.lower()
        # ==========================
        # APPROVE PACKAGE
        # ==========================

        approve_match = re.search(
            r"approve package (\d+)",
            msg
        )

        if approve_match:

            package_number = int(
                approve_match.group(1)
            )

            packages = list(
                generated_packages.values()
            )

            if package_number > len(packages):

                return {
                    "message":
                    "Invalid package number"
                }

            package = packages[
                package_number - 1
            ]

            package["status"] = "APPROVED"

            approved_packages[
                package["package_id"]
            ] = package

            return {
                "message":
                "Package approved",
                "package":
                package
            }
        # ==========================
        # PREPARE BOOKING
        # ==========================

        if "prepare booking" in msg:

            if not approved_packages:

                return {
                    "message":
                    "No approved package found"
                }

            package = list(
                approved_packages.values()
            )[-1]

            return FormService.prepare_booking(
                package
            )
        # ==========================
        # PREPARE BOOKING
        # ==========================

        if "prepare booking" in msg:

            if not approved_packages:

                return {
                    "message":
                    "No approved package found"
                }

            package = list(
                approved_packages.values()
            )[-1]

            return FormService.prepare_booking(
                package
            )
        # ==========================
        # EXECUTE BOOKING
        # ==========================

        if "execute booking" in msg:

            if not approved_packages:

                return {
                    "message":
                    "No approved package found"
                }

            package = list(
                approved_packages.values()
            )[-1]

            BookingService.execute_browser_filling(
                {
                    "booking_data":
                    package
                }
            )

            return {
                "message":
                "Browser automation started"
            }
        # SHOW PACKAGES
        if "show packages" in msg:

            packages = list(
                generated_packages.values()
            )

            return {
                "message":
                f"Found {len(packages)} packages",
                "packages":
                packages
            }

        # PACKAGE DETAILS
        if "package details" in msg:

            packages = list(
                generated_packages.values()
            )

            if not packages:

                return {
                    "message":
                    "No packages generated yet"
                }

            return {
                "message":
                "Package details",
                "package":
                packages[0]
            }

        # GENERATE PACKAGES

        details = self.extract_details(
            message
        )

        result = PackageGenerator.generate_packages(
            location=details["location"],
            guest_count=details["guest_count"],
            budget=details["budget"]
        )

        for index, package in enumerate(
            result["packages"],
            start=1
        ):
            package["display_id"] = index

        return result