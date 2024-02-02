from utils.error_handler import handle_exception
from scrapers.base.shopify_scraper import ShopifyScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from helpers.brand_normalizer import normalize_brand_name
from helpers.size_parser import parse_size
from helpers.product_type_verifier import verify_product_type
from helpers.country_name_validator import validate_country_name
from config.constants import UNKNOWN, MULTIPLE
from enums.product_type import ProductType
import requests
import re
from bs4 import BeautifulSoup
from helpers.variety_extractor import extract_varieties


class EightOunceCoffeeScraper(ShopifyScraper):
    def __init__(self, url, vendor, mock_data_path, product_base_url, home_url):
        super().__init__(url, vendor, mock_data_path, product_base_url, home_url)

    def process_products(self, fetched_products):
        # If fetched_products is provided, use it. Otherwise, use the products fetched by the base method
        products_to_process = fetched_products if fetched_products is not None else super().process_products()

        processed_products = []
        excluded_words = self.load_excluded_words()
        for product in products_to_process:
            try:
                processed_product_variants = []
                if not any(word in product["title"].lower() or word in product["handle"].lower() for word in excluded_words):
                    product_details = self.get_product_details(self.build_product_url(
                        product["handle"]))
                    processed_product = {
                        "brand": self.extract_brand(product, product_details),
                        "vendor": self.vendor,
                        "title": self.extract_title(product),
                        "handle": (handle := self.extract_handle(product)),
                        "product_url": (product_url := self.build_product_url(handle)),
                        "image_url": self.extract_image_url(product),
                        "is_decaf": self.is_decaf(product, product_details),
                        "product_type": self.extract_product_type(product, product_details),
                        "discovered_date_time": self.extract_published_date(product),
                        "country_of_origin": (country_of_origin := self.extract_country_of_origin(product_details)),
                        "continent": get_continent(country_of_origin),
                        "process": (process := self.extract_process(product_details)),
                        "process_category": self.get_process_category(process),
                        "tasting_notes": self.extract_notes(product_details),
                        "varieties": normalize_variety_names(self.extract_varieties(product_details))
                    }

                    for variant in product["variants"]:
                        processed_product_variant = {
                            "variant_id": self.extract_variant_id(
                                variant),
                            "size": self.extract_size(product, product_details),
                            "price": self.extract_price(
                                variant),
                            "is_sold_out": self.is_sold_out(
                                variant),
                        }
                        processed_product_variants.append(
                            processed_product_variant)

                    processed_product["variants"] = processed_product_variants
                    processed_products.append(processed_product)
            except Exception as e:
                handle_exception(e, context_info=f"Error processing product from vendor: {self.vendor}\n{product_url}")
                continue  # continue to next product

        return processed_products

    def extract_product_type(self, product, product_details):
        for detail in product_details:
            if 'format' in detail.lower():
                product_type = detail.split(':')[1].strip().title()
                if verify_product_type(product_type):
                    return product_type
                return ProductType.UNKNOWN

        lowercase_title = product["title"].lower()
        if 'instant' in lowercase_title:
            return ProductType.INSTANT.value
        elif 'capsule' in lowercase_title or 'box of' in lowercase_title:
            return ProductType.CAPSULE.value
        return ProductType.ROASTED_WHOLE_BEAN.value

    def get_product_details(self, product_url):
        # Fetch the page content
        response = requests.get(product_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with class that contains "main-product__block-label"
        main_info = soup.select('.main-product__block-label')

        # Find all elements with class that contains "main-product__block-text"
        seconday_info = soup.select('.main-product__block-text')

        # Extract the inner text from these elements
        main_details = [element.get_text(strip=True) for element in main_info]
        secondary_details = [element.get_text(
            strip=True) for element in seconday_info]

        return main_details + secondary_details

    def extract_title(self, product):
        if '-' in product["title"]:
            sub_title = product["title"].split('-', 1)[1].strip()
            if ':' in sub_title:
                return sub_title.split(':', 1)[0].strip().title()
            elif '(' in sub_title:
                return sub_title.split('(', 1)[0].strip().title()
            return sub_title.title()
        return product["title"].title()

    def extract_brand(self, product, product_details):
        if '-' in product["title"]:
            return normalize_brand_name(product["title"].split('-')[0].strip().title())

        for brand in self.coffee_brands:
            for detail in product_details:
                if brand in product["title"].lower() or brand in detail.lower():
                    return normalize_brand_name(brand.title())
        return UNKNOWN

    def extract_size(self, product, product_details):
        for detail in product_details:
            if 'quantity' in detail.lower():
                return parse_size(detail.split(':')[1].strip().lower())

        lowercase_title = product["title"].lower()
        if '(' in lowercase_title and ')' in lowercase_title:
            size_start = lowercase_title.rfind('(')
            size_end = lowercase_title.rfind(')')
            return parse_size(lowercase_title[size_start + 1: size_end].strip())

        for variant in product["variants"]:
            if variant["available"]:
                return variant["grams"]

        return 0

    def extract_country_of_origin(self, product_details):
        for detail in product_details:
            if 'origin' in detail.lower() and not 'origin type' in detail.lower():
                country_info = detail.split(':')[1].strip().title()
                if country_info == 'Blend':
                    return MULTIPLE
                return validate_country_name(country_info)
        return UNKNOWN

    def extract_varieties(self, product_details):
        for detail in product_details:
            if 'variety' in detail.lower():
                variety_info = detail.split(':')[1].strip().title()
                if variety_info != "":
                    variety_list = [x.strip().title()
                                    for x in re.split(',|&|/|And', variety_info)]
                    return extract_varieties(' '.join(variety_list))
                return [UNKNOWN]

        return [UNKNOWN]

    def extract_notes(self, product_details):
        for detail in product_details:
            if 'tasting notes' in detail.lower():
                tasting_notes = detail.split(':')[1].strip()
                if tasting_notes != "":
                    return [x.strip().title() for x in re.split(',|&', tasting_notes)]
                return [UNKNOWN]

        return [UNKNOWN]

    def extract_process(self, product_details):
        for detail in product_details:
            if 'process' in detail.lower():
                return detail.split(':')[1].strip().title()
        return UNKNOWN

    def build_product_url(self, handle):
        return f"{self.product_base_url}{handle}"

    def is_decaf(self, product, product_details):
        for detail in product_details:
            if 'full caffeine' in detail.lower():
                return False
            elif 'decaffeinated' in detail.lower():
                return True

        lowercase_title = product["title"].lower()
        keywords = self.load_decaf_words()
        for keyword in keywords:
            start_pos = lowercase_title.find(keyword)
            if start_pos != -1:
                break
        else:
            return False
        return True
