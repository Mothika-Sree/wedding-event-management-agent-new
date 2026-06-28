from app.data.package_store import (
    approved_packages,
    generated_packages
)

class ApprovalService:

    @staticmethod
    def approve_package(package_id: str):

        package = generated_packages.get(
            package_id
        )

        if not package:
            return {
                "error": "Package not found"
            }

        package["status"] = "APPROVED"

        approved_packages[
            package_id
        ] = package

        return package

    @staticmethod
    def get_status(package_id: str):

        return approved_packages.get(
            package_id,
            {
                "status": "NOT_FOUND"
            }
        )