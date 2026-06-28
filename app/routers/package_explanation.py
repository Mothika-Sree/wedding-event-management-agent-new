# app/routes/package_explanation.py

from fastapi import APIRouter

from app.data.package_store import generated_packages

router = APIRouter()


@router.get("/package-explanation/{package_id}")
def package_explanation(package_id: str):

    package = generated_packages.get(package_id)

    if not package:
        return {
            "error": "Package not found"
        }

    return {
        "package_id": package_id,
        "explanation": [
            f"Selected venue: {package['venue']}",
            f"Selected caterer: {package['caterer']}",
            f"Selected decorator: {package['decorator']}",
            f"Selected photographer: {package['photographer']}",
            f"Fits within budget with total cost ₹{package['total_cost']}",
            f"Package score: {package['package_score']}"
        ]
    
    }
@router.get("/compare-packages")
def compare_packages():

    packages = list(generated_packages.values())

    return {
        "packages": [
            {
                "package_id": p["package_id"],
                "venue": p["venue"],
                "cost": p["total_cost"],
                "score": p["package_score"]
            }
            for p in packages
        ]
    }