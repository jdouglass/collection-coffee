import requests
import json
from decimal import Decimal
from enums.continent import Continent
from enums.process_category import ProcessCategory
from config.constants import DEFAULT_IMAGE_URL


class CoffeeScraper:

    def __init__(self, url, vendor):
        self.url = url
        self.vendor = vendor
        self.products = []
        self.excluded_words = self.load_excluded_words()

    def load_excluded_words(self):
        with open('data/excluded_words.txt', 'r') as f:
            return [line.strip().lower() for line in f]

    def fetch_products(self):
        response = requests.get(self.url)
        data = response.json()
        self.products = data['products']

    @staticmethod
    def decimal_serializer(obj):
        """JSON serializer for objects not serializable by default json code."""
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, Continent):
            return obj.value
        raise TypeError("Type not serializable")

    def extract_published_date(self, product):
        return product["published_at"]

    def extract_image_url(self, product):
        return product["images"][0]["src"] if product["images"] else DEFAULT_IMAGE_URL

    def extract_handle(self, product):
        return product["handle"]

    def extract_price(self, product):
        return Decimal(product["variants"][0]["price"])

    def get_vendor(self, vendor):
        return vendor

    def extract_title(self, product):
        return product["title"].title()

    def is_sold_out(self, product):
        return not product["variants"][0]["available"]

    def get_process_category(self, body_html):
        process = self.extract_process(body_html)

        if ProcessCategory.WASHED.name in process:
            return ProcessCategory.WASHED.name
        elif ProcessCategory.NATURAL.name in process:
            return ProcessCategory.NATURAL.name
        elif process == ProcessCategory.UNKNOWN.name:
            return ProcessCategory.UNKNOWN.name
        else:
            return ProcessCategory.EXPERIMENTAL.name

    def display_products(self, products):
        print(json.dumps(products, default=self.decimal_serializer,
              indent=4, ensure_ascii=False))
