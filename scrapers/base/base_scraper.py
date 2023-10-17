import json
import requests
from decimal import Decimal
from enums.continent import Continent
from config.config import USE_MOCK_DATA


class BaseScraper:
    def __init__(self, url, vendor, mock_data_path):
        self.url = url
        self.vendor = vendor
        self.products = []
        self.excluded_words = self.load_excluded_words()
        self.mock_data_path = mock_data_path

    def load_excluded_words(self):
        with open('data/excluded_words.txt', 'r') as f:
            return [line.strip().lower() for line in f]

    def load_mock_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def fetch_products(self):
        if USE_MOCK_DATA:
            self.products = self.load_mock_data(self.mock_data_path)
            print(self.products)
        response = requests.get(self.url)
        data = response.json()
        self.products = data['products']
        print(self.products)

    def get_vendor(self, vendor):
        return vendor

    @staticmethod
    def decimal_serializer(obj):
        """JSON serializer for objects not serializable by default json code."""
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, Continent):
            return obj.value
        raise TypeError("Type not serializable")
