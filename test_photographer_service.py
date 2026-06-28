from app.services.wedmegood_photographer_service import (
    WedMeGoodPhotographerService
)

print(
    WedMeGoodPhotographerService.get_photographers()[:5]
)