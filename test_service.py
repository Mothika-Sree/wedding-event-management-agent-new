# test_service.py

from app.services.wedmegood_photographer_service import (
    WedMeGoodPhotographerService
)

print(
    WedMeGoodPhotographerService.get_photographers()
)