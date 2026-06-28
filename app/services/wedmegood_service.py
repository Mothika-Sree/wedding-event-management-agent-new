from app.scrapers.wedmegood_scraper import (
    WedMeGoodScraper
)

class WedMeGoodService:

    @staticmethod
    def get_venues():

        return WedMeGoodScraper.get_venues()