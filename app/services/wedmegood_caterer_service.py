from app.scrapers.wedmegood_caterer_scraper import (
    WedMeGoodCatererScraper
)


class WedMeGoodCatererService:

    @staticmethod
    def get_caterers():
        return WedMeGoodCatererScraper.get_caterers()