from app.scrapers.wedmegood_photographer_scraper import (
    WedMeGoodPhotographerScraper
)


class WedMeGoodPhotographerService:

    @staticmethod
    def get_photographers():
        return WedMeGoodPhotographerScraper.get_photographers()