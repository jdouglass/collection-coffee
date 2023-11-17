from enums.vendor_name import VendorName
from scrapers.vendor.traffic_coffee_scraper import TrafficCoffeeScraper
from scrapers.vendor.eight_ounce_coffee_scraper import EightOunceCoffeeScraper
from scrapers.vendor.revolver_coffee_scraper import RevolverCoffeeScraper
from scrapers.vendor.rogue_wave_coffee_scraper import RogueWaveCoffeeScraper
from scrapers.vendor.hatch_coffee_roasters_scraper import HatchCoffeeRoasterScraper
from scrapers.vendor.prototype_coffee_scraper import PrototypeCoffeeScraper

coffee_vendors_data = [
    {
        "key": VendorName.TRAFFIC.value,
        "home_url": "https://www.trafficcoffee.com",
        "url": "https://www.trafficcoffee.com/collections/our-coffees/products.json?limit=250",
        "product_base_url": "https://www.trafficcoffee.com/collections/our-coffees/products/",
        "vendor": VendorName.TRAFFIC.value,
        "scraper_class": TrafficCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/traffic_coffee.json",
        "mock_html_dom_path": "",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": VendorName.EIGHT_OUNCE.value,
        "home_url": "https://eightouncecoffee.ca",
        "url": "https://eightouncecoffee.ca/collections/all-coffee-bags/products.json?limit=250",
        "product_base_url": "https://eightouncecoffee.ca/products/",
        "vendor": VendorName.EIGHT_OUNCE.value,
        "scraper_class": EightOunceCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/eight_ounce_coffee.json",
        "mock_html_dom_path": "scrapers/mock_data/eight_ounce_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": VendorName.REVOLVER.value,
        "home_url": "https://revolvercoffee.ca",
        "url": "https://revolvercoffee.ca/collections/all-coffee/products.json?limit=250",
        "product_base_url": "https://revolvercoffee.ca/collections/all-coffee/products/",
        "vendor": VendorName.REVOLVER.value,
        "scraper_class": RevolverCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/revolver_coffee.json",
        "mock_html_dom_path": "",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": VendorName.ROGUE_WAVE.value,
        "home_url": "https://www.roguewavecoffee.ca",
        "url": "https://www.roguewavecoffee.ca/collections/coffee/products.json?limit=250",
        "product_base_url": "https://www.roguewavecoffee.ca/products/",
        "vendor": VendorName.ROGUE_WAVE.value,
        "scraper_class": RogueWaveCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/rogue_wave_coffee.json",
        "mock_html_dom_path": "scrapers/mock_data/rogue_wave_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": VendorName.HATCH.value,
        "home_url": "https://www.hatchcrafted.com",
        "url": "",
        "product_base_url": "https://www.hatchcrafted.com/shop/",
        "vendor": VendorName.HATCH.value,
        "scraper_class": HatchCoffeeRoasterScraper,
        "mock_data_path": "",
        "mock_html_dom_path": "",
        "currency": "CAD",
        "vendor_location": "Canada",
    },
    {
        "key": VendorName.PROTOTYPE.value,
        "home_url": "https://www.prototypecoffee.ca",
        "url": "https://www.prototypecoffee.ca/shop?format=json-pretty",
        "product_base_url": "https://prototypecoffee.ca/shop",
        "vendor": VendorName.PROTOTYPE.value,
        "scraper_class": PrototypeCoffeeScraper,
        "mock_data_path": "scrapers/mock_data/prototype_coffee.json",
        "mock_html_dom_path": "scrapers/mock_data/prototype_coffee.html",
        "currency": "CAD",
        "vendor_location": "Canada",
    }
]
