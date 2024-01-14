from scrapers.base.shopify_scraper import ShopifyScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from config.constants import UNKNOWN
from enums.product_type import ProductType
import requests
import re
from bs4 import BeautifulSoup
from helpers.variety_extractor import extract_varieties
from helpers.country_name_remover import remove_country_names
import traceback


class RogueWaveCoffeeScraper(ShopifyScraper):
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
                        "brand": self.vendor,
                        "vendor": self.vendor,
                        "title": self.extract_title(product),
                        "handle": (handle := self.extract_handle(product)),
                        "product_url": self.build_product_url(handle),
                        "image_url": self.extract_image_url(product),
                        "is_decaf": self.is_decaf(product),
                        "product_type": ProductType.ROASTED_WHOLE_BEAN.value,
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
                            "size": self.extract_size(variant, product["title"]),
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
                self.email_notifier.send_error_notification(error_message)

        return processed_products

    def get_product_details(self, product_url):
        response = requests.get(product_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        accordion_content = soup.find('div', class_="accordion__content rte")

        data = {}
        if accordion_content:
            for p_tag in accordion_content.find_all('p'):
                if p_tag.span:
                    key = p_tag.span.text.lower()
                    # Remove the span element to isolate the value
                    p_tag.span.decompose()
                    value = p_tag.text.strip()
                    data[key] = value.lower()

        taste_list = soup.find('ul', class_="product-taste-list")
        if taste_list:
            tastes = [li.get_text().strip().title()
                      for li in taste_list.find_all('li')]
            data['tasting_notes'] = tastes

        return data

    def extract_title(self, product):
        title = remove_country_names(product["title"])
        title = re.sub(r"\d+g", "", title).strip()
        title_parts = title.split("-")
        title = "-".join(part.strip() for part in title_parts if part.strip())
        if "|" in title:
            title = title.split("|")[0].strip()

        return title.strip()

    def extract_size(self, variant, title):
        size = parse_size(variant["title"])
        if (size == 0):
            size = parse_size(title.split('-')[-1])
        return size

    def extract_country_of_origin(self, product_details):
        if "origin" in product_details:
            return validate_country_name(product_details["origin"])
        return UNKNOWN

    def extract_varieties(self, product_details):
        if 'varieties' in product_details:
            variety_list = [x.strip().title()
                            for x in re.split(',|&|/|And', product_details["varieties"])]
            return extract_varieties(' '.join(variety_list))
        return [UNKNOWN]

    def extract_notes(self, product_details):
        if 'tasting_notes' in product_details:
            return product_details["tasting_notes"]
        return [UNKNOWN]

    def extract_process(self, product_details):
        if 'process' in product_details:
            return product_details["process"].title()
        return UNKNOWN

    def build_product_url(self, handle):
        return f"{self.product_base_url}{handle}"

    def is_decaf(self, product):
        lowercase_title = product["title"].lower()
        keywords = set(self.decaf_words)
        return any(keyword in lowercase_title for keyword in keywords)
