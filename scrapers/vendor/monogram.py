from scrapers.base.shopify_scraper import ShopifyScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from helpers.brand_normalizer import normalize_brand_name
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from config.constants import UNKNOWN, MULTIPLE
from enums.product_type import ProductType
import requests
import re
from bs4 import BeautifulSoup
from helpers.variety_extractor import extract_varieties
import traceback
from config.config import DEVELOPMENT_MODE
from config.logger_config import logger


class MonogramScraper(ShopifyScraper):
    def __init__(self, url, vendor, mock_data_path, product_base_url, home_url):
        super().__init__(url, vendor, mock_data_path, product_base_url, home_url)

    def process_products(self, fetched_products):
        products_to_process = fetched_products if fetched_products is not None else super().process_products()

        processed_products = []
        product_urls = self.get_product_urls(self.product_base_url)
        for product in products_to_process:
            if self.is_valid_product(product["title"]):
                handle = self.extract_handle(product)
                product_url = self.build_product_url(handle, product_urls)
                try:
                    processed_product_variants = []
                    product_details = self.get_product_details(product_url)
                    # print(product_details)
                    processed_product = {
                        "brand": self.extract_brand(product),
                        "vendor": self.vendor,
                        "title": self.extract_title(product),
                        "handle": handle,
                        "product_url": product_url,
                        "image_url": self.extract_image_url(product),
                        "is_decaf": self.is_decaf(product["title"]),
                        "product_type": ProductType.ROASTED_WHOLE_BEAN.value,
                        "discovered_date_time": self.extract_published_date(product),
                        "country_of_origin": (country_of_origin := self.extract_country_of_origin(product, product_details)),
                        "continent": get_continent(country_of_origin),
                        "process": (process := self.extract_process(product, product_details)),
                        "process_category": self.get_process_category(process),
                        "tasting_notes": product_details["tasting_notes"],
                        "varieties": normalize_variety_names(self.extract_varieties(product, product_details))
                    }

                    for variant in product["variants"]:
                        processed_product_variant = {
                            "variant_id": self.extract_variant_id(
                                variant),
                            "size": self.extract_size(variant),
                            "price": self.extract_price(
                                variant),
                            "is_sold_out": self.is_sold_out(
                                variant),
                        }
                        processed_product_variants.append(
                            processed_product_variant)

                    processed_product["variants"] = processed_product_variants
                    processed_products.append(processed_product)
                except Exception:
                    error_message = f"{self.vendor}\n\n{traceback.format_exc()}"
                    if not DEVELOPMENT_MODE:
                        self.email_notifier.send_error_notification(
                            error_message)
                    logger.error(error_message)

        return processed_products

    def get_product_urls(self, product_base_url):
        response = requests.get(f"{product_base_url}/whole-bean-coffee")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        h4_elements = soup.find_all('h4', class_='product-item__product-title')
        urls = [
            f"{self.home_url}{h4.find('a')['href']}" for h4 in h4_elements if h4.find('a')]

        return urls

    def get_product_details(self, product_url):
        response = requests.get(product_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract tasting notes
        first_element = soup.find(
            "div", class_="product__description product__block product__block--medium")
        next_element = first_element.find_next_sibling()
        tasting_notes = [item.get_text().strip().title() for item in next_element.find_all(
            "div", class_="product__callouts-mini-item-text")]

        # Extract body content and split by line breaks
        body_content_div = soup.find("div", class_="product__callouts-items")
        body_content = body_content_div.get_text(separator="\n").split("\n")
        # Remove empty lines
        body_content = [line.strip() for line in body_content if line.strip()]

        return {
            'tasting_notes': tasting_notes,
            'body_content': body_content
        }

    def extract_title(self, product):
        if 'Atlas Coffee Program -' in product["title"]:
            return product["title"].replace("Atlas Coffee Program -", "").strip()
        return product["title"]

    def extract_brand(self, product):
        if 'Atlas Coffee Program' in product["title"]:
            return normalize_brand_name(product["title"].split('-')[1].strip())
        return self.vendor

    def extract_country_of_origin(self, product, product_details):
        if 'ORIGIN:' in product["body_html"]:
            return validate_country_name(product["body_html"].split("ORIGIN:")[1].split('<')[0].strip())
        for content in product_details["body_content"]:
            if 'Country:' in content:
                return validate_country_name(content.replace('Origin:', '').strip())
        return UNKNOWN

    def extract_varieties(self, product, product_details):
        if 'VARIETY:' in product["body_html"]:
            varieties = product["body_html"].split(
                'VARIETY:')[1].split('<')[0].strip()
            # print(varieties)
            variety_list = [x.strip().title() for x in varieties.split(',')]
            # print(variety_list)
            return extract_varieties(' '.join(variety_list))
        for content in product_details["body_content"]:
            # print("in here")
            if 'Variety:' in content:
                varieties = content.replace('Variety:', '').strip()
                variety_list = [x.strip().title()
                                for x in varieties.split(',')]
                return extract_varieties(' '.join(variety_list))
        return [UNKNOWN]

    def extract_process(self, product, product_details):
        if 'PROCESS:' in product["body_html"]:
            return product["body_html"].split('PROCESS:')[1].split('<')[0].strip().title()
        for content in product_details["body_content"]:
            if 'Process:' in content:
                return content.replace('Process:', '').strip().title()
        return UNKNOWN

    def build_product_url(self, handle, product_urls):
        return next((url for url in product_urls if handle in url), None)
