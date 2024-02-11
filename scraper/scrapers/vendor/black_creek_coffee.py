from utils.error_handler import handle_exception
from scrapers.base.shopify_scraper import ShopifyScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from config.constants import UNKNOWN
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from enums.product_type import ProductType
from helpers.variety_extractor import extract_varieties
import re

class BlackCreekCoffeeScraper(ShopifyScraper):
    def __init__(self, url, vendor, mock_data_path, product_base_url, home_url):
        super().__init__(url, vendor, mock_data_path, product_base_url, home_url)

    def process_products(self, fetched_products):
        # If fetched_products is provided, use it. Otherwise, use the products fetched by the base method
        products_to_process = fetched_products if fetched_products is not None else super().process_products()

        processed_products = []
        excluded_words = self.load_excluded_words()
        for product in products_to_process:
            if not any(word in product["title"].lower() or word in product["handle"].lower() for word in excluded_words):
                try:
                    processed_product_variants = []
                    processed_product = {
                        "brand": self.vendor,
                        "vendor": self.vendor,
                        "title": self.extract_title(product),
                        "handle": (handle := self.extract_handle(product)),
                        "product_url": self.build_product_url(handle),
                        "image_url": self.extract_image_url(product),
                        "is_decaf": self.is_decaf(product["title"]),
                        "product_type": ProductType.ROASTED_WHOLE_BEAN.value,
                        "discovered_date_time": self.extract_published_date(
                            product),
                        "country_of_origin": (country_of_origin := self.extract_country_of_origin(
                            product)),
                        "continent": get_continent(country_of_origin),
                        "process": (process := self.extract_process(product["body_html"])),
                        "process_category": UNKNOWN if '?' in process else self.get_process_category(process),
                        "tasting_notes": [UNKNOWN],
                        "varieties": normalize_variety_names(self.extract_varieties(product["body_html"])),
                    }

                    for variant in product["variants"]:
                        variant_size = self.extract_size(variant)
                        if any(variant_size == processed_variant['size'] for processed_variant in processed_product_variants):
                            continue
                        processed_product_variant = {
                            "variant_id": self.extract_variant_id(
                                variant),
                            "size": variant_size,
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
                    handle_exception(e, context_info=f"Error processing product from vendor: {self.vendor}\n{self.build_product_url(handle)}")

        return processed_products

    def _extract_from_body(self, body_html, keywords):
        for keyword in keywords:
            start_pos = body_html.find(keyword)
            if start_pos != -1:
                break
        else:
            return UNKNOWN
        start_pos = body_html.find(":", start_pos) + 1
        info = body_html[start_pos:].strip()
        for tag in ['<span>', '</span>', '<strong>', '</strong>', '<span data-mce-fragment=\"1\">']:
            info = info.replace(tag, '')
        return info.split('<')[0].strip()

    def extract_size(self, variant):
        return parse_size(variant["title"].split("-")[0].strip())

    def extract_country_of_origin(self, product):
        country_info = validate_country_name(product["title"])
        if country_info == "Unknown":
            keywords = ["Blend:"]
            country_info = self._extract_from_body(product["body_html"], keywords)
        return validate_country_name(country_info)

    def extract_varieties(self, body_html):
        keywords = ["Variety"]
        variety_info = self._extract_from_body(body_html, keywords)
        variety_info = variety_info.replace("&amp;", ", ")
        variety_info = variety_info.replace("/", ",")
        variety_info = variety_info.replace("Arabica", "")
        if variety_info == "" or '?' in variety_info:
            return [UNKNOWN]
        variety_list = [x.strip().title()
                        for x in re.split(',|/|&', variety_info)]
        return extract_varieties(' '.join(variety_list))

    def extract_process(self, body_html):
        keywords = ["Process"]
        process_info = self._extract_from_body(body_html, keywords)
        if process_info == "" or '?' in process_info:
            return UNKNOWN
        process_info = process_info.replace('&amp;', ',')
        process_info = process_info.replace(" ,", ",")
        return process_info.title().strip()

    def build_product_url(self, handle):
        return f"{self.product_base_url}/{handle}"

    def is_decaf(self, title):
        formatted_title = title.lower()
        for keyword in self.decaf_words:
            start_pos = formatted_title.find(keyword)
            if start_pos != -1:
                break
        else:
            return False
        return True
