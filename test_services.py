from app.services.wedmegood_service import WedMeGoodService
from app.services.wedmegood_caterer_service import WedMeGoodCatererService
from app.services.wedmegood_decorator_service import WedMeGoodDecoratorService
from app.services.wedmegood_photographer_service import WedMeGoodPhotographerService

print("Venue Service:")
print(len(WedMeGoodService.get_venues()))

print("Caterer Service:")
print(len(WedMeGoodCatererService.get_caterers()))

print("Decorator Service:")
print(len(WedMeGoodDecoratorService.get_decorators()))

print("Photographer Service:")
print(len(WedMeGoodPhotographerService.get_photographers()))