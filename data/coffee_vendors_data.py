from scrapers.vendor.traffic_coffee_scraper import TrafficCoffeeScraper
from scrapers.vendor.eight_ounce_coffee_scraper import EightOunceCoffeeScraper

coffee_vendors_data = [
    {
        "key": "Traffic Coffee",
        "url": "https://www.trafficcoffee.com/collections/our-coffees/products.json?limit=250",
        "vendor": "Traffic Coffee",
        "scraper_class": TrafficCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/traffic_coffee.json",
        "mock_html_dom_path": "",
        "currency": "CAD",
        "vendor_location": "Canada"
    },
    {
        "key": "Eight Ounce Coffee",
        "url": "https://eightouncecoffee.ca/collections/newest-coffee/products.json?limit=250",
        "vendor": "Eight Ounce Coffee",
        "scraper_class": EightOunceCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/eight_ounce_coffee.json",
        "mock_html_dom_path": "scrapers/mock_data/eight_ounce_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada"
    }
    # Add more vendor data as needed
]
