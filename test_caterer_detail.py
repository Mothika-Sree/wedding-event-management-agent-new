from pprint import pprint

from app.scrapers.wedmegood_caterer_detail_scraper import (
    WedMeGoodCatererDetailScraper
)


url = (
    "https://www.wedmegood.com/profile/"
    "Party-Planners-Caterers-1443384"
)

result = (
    WedMeGoodCatererDetailScraper
    .get_caterer_details(url)
)

pprint(result)