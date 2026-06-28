from pprint import pprint
from app.scrapers.wedmegood_photographer_detail_scraper import (
    WedMeGoodPhotographerDetailScraper
)

url = "https://www.wedmegood.com/profile/Jaishankar-Natarajan-Photography-181492"

details = WedMeGoodPhotographerDetailScraper.get_photographer_details(url)

pprint(details)