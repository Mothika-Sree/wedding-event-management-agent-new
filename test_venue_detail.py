from pprint import pprint

from app.scrapers.wedmegood_venue_detail_scraper import (
    WedMeGoodVenueDetailScraper
)

url = "https://www.wedmegood.com/wedding-venues/Kailash-Resort-742051"

result = WedMeGoodVenueDetailScraper.get_venue_details(url)

pprint(result)