from app.scrapers.wedmegood_scraper import (
    WedMeGoodScraper
)

venues = WedMeGoodScraper.get_venues()

for venue in venues[:2]:
    print(venue)