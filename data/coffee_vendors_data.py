from scrapers.vendor.traffic_coffee_scraper import TrafficCoffeeScraper
from scrapers.vendor.eight_ounce_coffee_scraper import EightOunceCoffeeScraper
from scrapers.vendor.revolver_coffee_scraper import RevolverCoffeeScraper
from scrapers.vendor.rogue_wave_coffee_scraper import RogueWaveCoffeeScraper
from scrapers.vendor.hatch_coffee_roasters_scraper import HatchCoffeeRoasterScraper

coffee_vendors_data = [
    {
        "key": "Traffic Coffee",
        "home_url": "https://www.trafficcoffee.com",
        "url": "https://www.trafficcoffee.com/collections/our-coffees/products.json?limit=250",
        "product_base_url": "https://www.trafficcoffee.com/collections/our-coffees/products/",
        "vendor": "Traffic Coffee",
        "scraper_class": TrafficCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/traffic_coffee.json",
        "mock_html_dom_path": "",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": "Eight Ounce Coffee",
        "home_url": "https://eightouncecoffee.ca",
        "url": "https://eightouncecoffee.ca/collections/all-coffee-bags/products.json?limit=250",
        "product_base_url": "https://eightouncecoffee.ca/products/",
        "vendor": "Eight Ounce Coffee",
        "scraper_class": EightOunceCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/eight_ounce_coffee.json",
        "mock_html_dom_path": "scrapers/mock_data/eight_ounce_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": "Revolver Coffee",
        "home_url": "https://revolvercoffee.ca",
        "url": "https://revolvercoffee.ca/collections/all-coffee/products.json?limit=250",
        "product_base_url": "https://revolvercoffee.ca/collections/all-coffee/products/",
        "vendor": "Revolver Coffee",
        "scraper_class": RevolverCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/revolver_coffee.json",
        "mock_html_dom_path": "",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": "Rogue Wave Coffee",
        "home_url": "https://www.roguewavecoffee.ca",
        "url": "https://www.roguewavecoffee.ca/collections/coffee/products.json?limit=250",
        "product_base_url": "https://www.roguewavecoffee.ca/products/",
        "vendor": "Rogue Wave Coffee",
        "scraper_class": RogueWaveCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/rogue_wave_coffee.json",
        "mock_html_dom_path": "scrapers/mock_data/rogue_wave_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": "Hatch Coffee Roasters",
        "home_url": "https://www.hatchcrafted.com",
        "url": "",
        "product_base_url": "https://www.hatchcrafted.com/shop/",
        "vendor": "Hatch Coffee Roasters",
        "scraper_class": HatchCoffeeRoasterScraper,
        "mock_data_path": "",
        "mock_html_dom_path": "scrapers/mock_data/rogue_wave_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada",
    }
]
