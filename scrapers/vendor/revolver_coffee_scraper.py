from scrapers.base.shopify_scraper import ShopifyScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from helpers.brand_normalizer import normalize_brand_name
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from config.constants import UNKNOWN
from enums.product_type import ProductType
import re
from helpers.variety_extractor import extract_varieties
from helpers.title_formatter import title_formatter
import pycountry
from enums.process_category import ProcessCategory
import traceback


class RevolverCoffeeScraper(ShopifyScraper):
    VARIETIES_KEYWORD = "variet"
    NOTES_KEYWORD = "notes"
    PROCESS_KEYWORD = "process"

    def __init__(self, url, vendor, mock_data_path, product_base_url):
        super().__init__(url, vendor, mock_data_path, product_base_url)
        self.coffee_brands = self.load_coffee_brands()

    def process_products(self, fetched_products):
        # If fetched_products is provided, use it. Otherwise, use the products fetched by the base method
        products_to_process = fetched_products if fetched_products is not None else super().process_products()

        processed_products = []
        excluded_words = self.load_excluded_words()
        for product in products_to_process:
            try:

                processed_product_variants = []
                if not any(word in product["title"].lower() or word in product["handle"].lower() for word in excluded_words):
                    # Creating a new product dictionary with only the required fields
                    processed_product = {
                        "brand": self.extract_brand(product),
                        "vendor": self.get_vendor(self.vendor),
                        "title": self.extract_title(product),
                        "handle": (handle := self.extract_handle(product)),
                        "product_url": self.build_product_url(handle),
                        "image_url": self.extract_image_url(product),
                        "is_decaf": self.is_decaf(product),
                        "product_type": self.extract_product_type(product),
                        "discovered_date_time": self.extract_published_date(product),
                        "country_of_origin": (country_of_origin := self.extract_country_of_origin(product)),
                        "continent": get_continent(country_of_origin),
                        "process": (process := self.extract_process(product)),
                        "process_category": self.get_process_category(process),
                        "tasting_notes": self.extract_notes(product),
                        "varieties": normalize_variety_names(self.extract_varieties(product))
                    }

                    for variant in product["variants"]:
                        processed_product_variant = {
                            "variant_id": self.extract_variant_id(
                                variant),
                            "size": self.extract_size(product),
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
                error_message = traceback.format_exc()
                self.email_notifier.send_error_notification(error_message)

        return processed_products

    def extract_product_type(self, product):
        lowercase_title = product["title"].lower()
        if ProductType.INSTANT.value.lower() in lowercase_title:
            return ProductType.INSTANT.value
        elif ProductType.CAPSULE.value.lower() in lowercase_title or 'pods' in lowercase_title:
            return ProductType.CAPSULE.value
        return ProductType.ROASTED_WHOLE_BEAN.value

    def extract_title(self, product):
        title = product["title"]
        if "*" in title:
            title = title.split("*")[0].strip()
        if "'" in title:
            title = title.replace("'", "").strip()
        if "\"" in title:
            title = title.replace("\"", "").strip()

        for brand in self.coffee_brands:
            title = title.lower().replace(brand.lower(), "", 1).strip()

        # Get a list of all country names
        countries = sorted(
            [country.name for country in pycountry.countries], key=len, reverse=True)

        for country in countries:
            title = title.replace(country.lower(), "").strip()

        return title_formatter(title)

    def extract_brand(self, product):
        brand_name = next(
            (normalize_brand_name(brand) for brand in self.coffee_brands
             if brand.lower() in product["title"].lower()),
            UNKNOWN
        )
        return brand_name.title()

    def extract_size(self, product):
        search_patterns = {
            'kg': r'\d+kg',
            'g': r'\d+g',
            'pods': r'\d+ pods',
            'packs': r'\d+ packs',
            'grams': lambda p: p["variants"][0]["grams"]
        }

        for unit, pattern in search_patterns.items():
            if callable(pattern):
                size = pattern(product)
            else:
                match = re.search(
                    pattern, (product["title"] + product["body_html"]).lower())
                size = match.group() if match else None
            if size:
                return parse_size(size)
        if product["variants"][0]["grams"]:
            return product["variants"][0]["grams"]
        return 0

    def extract_country_of_origin(self, product):
        cleaned_title = product["title"]
        if "*" in cleaned_title:
            cleaned_title = cleaned_title.split("*")[0].strip()
        for brand in self.coffee_brands:
            if brand.lower() in cleaned_title.lower():
                cleaned_title = cleaned_title.lower().replace(brand, "").strip()
        country = validate_country_name(cleaned_title)

        if country != UNKNOWN:
            return country
        if "note" in product["body_html"].lower():
            components = product["body_html"].lower().split("note")[0]
            country = validate_country_name(components)
            if country != UNKNOWN:
                return country
            else:
                return validate_country_name(product["handle"])
        return UNKNOWN

    def extract_varieties(self, product):
        varieties = self.extract_html_body_content(
            product, self.VARIETIES_KEYWORD)
        if varieties:
            varieties = [x.strip().title() for x in re.split(
                ',|/|\+|&amp;| and ', varieties)]
            return extract_varieties(' '.join(varieties))
        return [UNKNOWN]

    def extract_notes(self, product):
        notes = self.extract_html_body_content(product, self.NOTES_KEYWORD)
        if notes:
            return [title_formatter(x.strip()) for x in re.split(',|/|\+|&amp;| and ', notes)]
        return [UNKNOWN]

    def extract_process(self, product):
        process = self.extract_html_body_content(product, self.PROCESS_KEYWORD)
        if process:
            return process.title()

        # Check for process in title if not found in body_html
        for process_category in ProcessCategory:
            if process_category.value.lower() in product["title"].lower():
                return process_category.value
        return UNKNOWN

    def extract_html_body_content(self, product, keyword):
        body_html = product["body_html"].lower()
        if keyword in body_html:
            content = body_html.split(keyword)[1]

            tags_to_remove = [
                "<meta charset=\"utf-8\">",
                "<span data-mce-fragment=\"1\">"
            ]

            for tag in tags_to_remove:
                content = content.replace(tag, "")

            return content.split(":")[1].split("<")[0].strip()
        return ""

    def build_product_url(self, handle):
        return f"{self.product_base_url}{handle}"

    def is_decaf(self, product):
        decaf_keywords = self.load_decaf_words()
        content = (product["title"] + product["body_html"]).lower()
        return any(keyword in content for keyword in decaf_keywords)
