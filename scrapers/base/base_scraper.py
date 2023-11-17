import json
from decimal import Decimal
from enums.continent import Continent
from enums.process_category import ProcessCategory
from config.logger_config import logger
from utils.email_notifier import EmailNotifier
from datetime import datetime


class BaseScraper:
    def __init__(self, url, vendor, mock_data_path, product_base_url, home_url):
        self.url = url
        self.vendor = vendor
        self.products = []
        self.mock_data_path = mock_data_path
        self.product_base_url = product_base_url
        self.email_notifier = EmailNotifier()
        self.coffee_brands = self.load_coffee_brands()
        self.decaf_words = self.load_decaf_words()
        self.home_url = home_url

    def load_excluded_words(self):
        with open('data/excluded_words.txt', 'r') as f:
            return [line.strip().lower() for line in f]

    def load_decaf_words(self):
        with open('data/decaf_words.txt', 'r') as f:
            return [line.strip().lower() for line in f]

    def load_coffee_brands(self):
        with open('data/coffee_brands.txt', 'r') as f:
            return [line.strip().lower() for line in f]

    def load_mock_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_vendor(self, vendor):
        return vendor

    def get_process_category(self, process):
        categories = [ProcessCategory.WASHED.value,
                      ProcessCategory.NATURAL.value, ProcessCategory.HONEY.value]

        if process == ProcessCategory.UNKNOWN.value:
            return ProcessCategory.UNKNOWN.value

        found_categories = [cat for cat in categories if cat in process]

        if len(found_categories) >= 2:
            return ProcessCategory.EXPERIMENTAL.value
        elif len(found_categories) == 1:
            return found_categories[0]
        else:
            return ProcessCategory.EXPERIMENTAL.value

    def is_decaf(self, title):
        lowercase_title = title.lower()
        keywords = set(self.decaf_words)
        return any(keyword in lowercase_title for keyword in keywords)

    @staticmethod
    def decimal_serializer(obj):
        """JSON serializer for objects not serializable by default json code."""
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, Continent):
            return obj.value
        if isinstance(obj, datetime):
            return str(obj)
        raise TypeError("Type not serializable")

    def display_products(self, products):
        logger.debug(json.dumps(
            products, default=self.decimal_serializer, indent=4, ensure_ascii=False))
