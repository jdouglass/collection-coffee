import json
import requests
from decimal import Decimal
from enums.continent import Continent
from config.config import USE_MOCK_DATA
from enums.process_category import ProcessCategory
from config.logger_config import logger


class BaseScraper:
    def __init__(self, url, vendor, mock_data_path, product_base_url):
        self.url = url
        self.vendor = vendor
        self.products = []
        self.mock_data_path = mock_data_path
        self.product_base_url = product_base_url

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

    def fetch_products(self):
        if USE_MOCK_DATA:
            self.products = self.load_mock_data(self.mock_data_path)
            return
        response = requests.get(self.url)
        data = response.json()
        self.products = data['products']

    def get_vendor(self, vendor):
        return vendor

    def get_process_category(self, process):
        if ProcessCategory.WASHED.value in process and ProcessCategory.NATURAL.value in process or \
                ProcessCategory.WASHED.value in process and ProcessCategory.HONEY.value in process or \
                ProcessCategory.NATURAL.value in process and ProcessCategory.HONEY.value in process:
            return ProcessCategory.EXPERIMENTAL.value
        elif ProcessCategory.WASHED.value in process and ProcessCategory.HONEY.value in process:
            return ProcessCategory.EXPERIMENTAL.value
        elif ProcessCategory.WASHED.value in process:
            return ProcessCategory.WASHED.value
        elif ProcessCategory.NATURAL.value in process:
            return ProcessCategory.NATURAL.value
        elif ProcessCategory.HONEY.value in process:
            return ProcessCategory.HONEY.value
        elif process == ProcessCategory.UNKNOWN.value:
            return ProcessCategory.UNKNOWN.value
        else:
            return ProcessCategory.EXPERIMENTAL.value

    @staticmethod
    def decimal_serializer(obj):
        """JSON serializer for objects not serializable by default json code."""
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, Continent):
            return obj.value
        raise TypeError("Type not serializable")

    def display_products(self, products):
        logger.debug(json.dumps(
            products, default=self.decimal_serializer, indent=4, ensure_ascii=False))
