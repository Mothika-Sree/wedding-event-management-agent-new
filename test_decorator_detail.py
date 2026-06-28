from pprint import pprint
from app.scrapers.wedmegood_decorator_detail_scraper import (
    WedMeGoodDecoratorDetailScraper
)

url = "https://www.wedmegood.com/profile/Happy-Moments-25147627"

details = WedMeGoodDecoratorDetailScraper.get_decorator_details(url)

pprint(details)