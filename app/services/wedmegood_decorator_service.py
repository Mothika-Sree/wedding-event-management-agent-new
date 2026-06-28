from app.scrapers.wedmegood_decorator_scraper import (
    WedMeGoodDecoratorScraper
)


class WedMeGoodDecoratorService:

    @staticmethod
    def get_decorators():
        return WedMeGoodDecoratorScraper.get_decorators()