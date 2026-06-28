from app.services.wedmegood_caterer_service import (
    WedMeGoodCatererService
)

from app.services.vendor_ranking_service import (
    VendorRankingService
)

vendors = WedMeGoodCatererService.get_caterers()

ranked = VendorRankingService.rank_vendors(
    vendors,
    budget=400,
    guest_count=500,
    location="Chennai"
)

for vendor in ranked[:5]:
    print(vendor)