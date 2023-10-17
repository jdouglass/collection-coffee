from scrapers.vendor.traffic_coffee_scraper import TrafficCoffeeScraper

coffee_vendors_data = [
    {
        "key": "Traffic Coffee",
        "url": "https://www.trafficcoffee.com/collections/our-coffees/products.json?limit=250",
        "vendor": "Traffic Coffee",
        "scraper_class": TrafficCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/traffic_coffee.json",
        "mock_html_dom_path": "traffic_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada"
    }
    # Add more vendor data as needed
]
