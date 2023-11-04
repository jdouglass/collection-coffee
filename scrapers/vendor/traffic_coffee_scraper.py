from scrapers.base.shopify_scraper import ShopifyScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from config.constants import UNKNOWN
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from enums.product_type import ProductType
from helpers.variety_extractor import extract_varieties
import re


class TrafficCoffeeScraper(ShopifyScraper):
    def __init__(self, url, vendor, mock_data_path, product_base_url):
        super().__init__(url, vendor, mock_data_path, product_base_url)
        self.coffee_brands = self.load_coffee_brands()

    def process_products(self, fetched_products):
        # If fetched_products is provided, use it. Otherwise, use the products fetched by the base method
        products_to_process = fetched_products if fetched_products is not None else super().process_products()

        processed_products = []
        for product in products_to_process:
            # Creating a new product dictionary with only the required fields
            processed_product = {}
            processed_product["vendor"] = self.get_vendor(self.vendor)
            processed_product["brand"] = self.extract_brand()
            processed_product["title"] = self.extract_title(product)
            processed_product["weight"] = self.extract_weight(product)
            processed_product["product_url"] = self.build_product_url(
                product["handle"])
            processed_product["image_url"] = self.extract_image_url(product)
            processed_product["is_sold_out"] = self.is_sold_out(product)
            processed_product["is_decaf"] = self.is_decaf(product["title"])
            processed_product["product_type"] = ProductType.ROASTED_WHOLE_BEAN.value
            processed_product["discovered_date_time"] = self.extract_published_date(
                product)
            processed_product["handle"] = self.extract_handle(product)
            processed_product["price"] = self.extract_price(product)

            body_html = product.get("body_html", "")
            processed_product["country_of_origin"] = self.extract_country_of_origin(
                body_html)
            processed_product["continent"] = get_continent(
                processed_product["country_of_origin"])
            processed_product["process"] = self.extract_process(body_html)
            processed_product["process_category"] = UNKNOWN if '?' in processed_product["process"] else self.get_process_category(
                processed_product["process"])
            processed_product["tasting_notes"] = self.extract_notes(body_html)
            processed_product["varieties"] = normalize_variety_names(
                self.extract_varieties(body_html))

            processed_products.append(processed_product)

        return processed_products

    def extract_brand(self):
        return self.vendor

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

    def extract_weight(self, product):
        for variant in product["variants"]:
            if variant["available"]:
                return parse_size(variant["title"])
            else:
                return parse_size(product["variants"][0]["title"])
        return 0

    def extract_country_of_origin(self, body_html):
        keywords = ["Origin"]
        country_info = self._extract_from_body(body_html, keywords)
        country_info = country_info.split(',')[-1].strip()
        return validate_country_name(country_info)

    def extract_varieties(self, body_html):
        keywords = ["Varietal", "Variety", "Varietals", "Varieties", "Variété"]
        variety_info = self._extract_from_body(body_html, keywords)
        variety_info = variety_info.replace(" &amp; ", ", ")
        variety_info = variety_info.replace("/", ",")
        if variety_info == "" or '?' in variety_info:
            return [UNKNOWN]
        variety_list = [x.strip().title()
                        for x in re.split(',|/|&', variety_info)]
        return extract_varieties(' '.join(variety_list))

    def extract_notes(self, body_html):
        keywords = ["Notes", "In the cup"]
        notes_info = self._extract_from_body(body_html, keywords)
        if notes_info == "":
            return [UNKNOWN]
        return [x.strip().title() for x in re.split(',|/', notes_info)]

    def extract_process(self, body_html):
        keywords = ["Process"]
        process_info = self._extract_from_body(body_html, keywords)
        if process_info == "" or '?' in process_info:
            return UNKNOWN
        process_info = process_info.replace('&amp;', ',')
        process_info = process_info.replace(" ,", ",")
        return process_info.title().strip()

    def build_product_url(self, handle):
        return f"{self.product_base_url}{handle}"

    def is_decaf(self, title):
        formatted_title = title.lower()
        keywords = self.load_decaf_words()
        for keyword in keywords:
            start_pos = formatted_title.find(keyword)
            if start_pos != -1:
                break
        else:
            return False
        return True
