from decimal import Decimal
from config.constants import DEFAULT_IMAGE_URL
from scrapers.base.base_scraper import BaseScraper
from config.config import USE_MOCK_DATA
import requests
from datetime import datetime


class SquareSpaceScraper(BaseScraper):

    def extract_published_date(self, product):
        # Divide by 1000 to convert the timestamp from milliseconds to seconds
        # because Python can only accept unix timestamp in seconds
        return datetime.fromtimestamp(product["publishOn"] / 1000)

    def extract_image_url(self, product):
        return product["items"][0]["assetUrl"] if product["items"][0]["assetUrl"] else DEFAULT_IMAGE_URL

    def extract_handle(self, product):
        return product["urlId"]

    def extract_price(self, variant):
        return Decimal(variant["priceMoney"]["value"])

    def extract_title(self, product):
        return product["title"].title()

    def is_sold_out(self, variant):
        return not variant["unlimited"]

    def extract_variant_id(self, variant):
        return variant["id"]

    def fetch_products(self):
        if USE_MOCK_DATA:
            self.products = self.load_mock_data(self.mock_data_path)
            return
        response = requests.get(self.url)
        data = response.json()
        self.products = data['items']
