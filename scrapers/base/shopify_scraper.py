from decimal import Decimal
from config.constants import DEFAULT_IMAGE_URL
from scrapers.base.base_scraper import BaseScraper
from enums.product_type import ProductType


class ShopifyScraper(BaseScraper):

    def extract_published_date(self, product):
        return product["published_at"]

    def extract_image_url(self, product):
        return product["images"][0]["src"] if product["images"] else DEFAULT_IMAGE_URL

    def extract_handle(self, product):
        return product["handle"]

    def extract_price(self, variant):
        return Decimal(variant["price"])

    def extract_title(self, product):
        return product["title"].title()

    def is_sold_out(self, variant):
        return not variant["available"]

    def extract_product_id(self, variant):
        return variant["product_id"]

    def extract_variant_id(self, variant):
        return variant["id"]

    def extract_size(self, variant):
        return variant["grams"]
