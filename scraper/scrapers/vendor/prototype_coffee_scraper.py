from utils.error_handler import handle_exception
from scrapers.base.square_space_scraper import SquareSpaceScraper
from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from config.constants import UNKNOWN
from enums.product_type import ProductType
import re
from bs4 import BeautifulSoup
from helpers.variety_extractor import extract_varieties


class PrototypeCoffeeScraper(SquareSpaceScraper):
    def __init__(self, url, vendor, mock_data_path, product_base_url, home_url):
        super().__init__(url, vendor, mock_data_path, product_base_url, home_url)

    def process_products(self, fetched_products):
        # If fetched_products is provided, use it. Otherwise, use the products fetched by the base method
        products_to_process = fetched_products if fetched_products is not None else super().process_products()

        processed_products = []
        for product in products_to_process:
            try:
                processed_product_variants = []
                title = self.extract_title(product)
                if not any(word in title.lower() for word in self.excluded_words):
                    handle = self.extract_handle(product)
                    product_url = self.build_product_url(handle)
                    product_details = self.get_product_details(product_url)
                    processed_product = {
                        "brand": self.vendor,
                        "vendor": self.vendor,
                        "title": title,
                        "handle": handle,
                        "product_url": product_url,
                        "image_url": self.extract_image_url(product),
                        "is_decaf": self.is_decaf(product["title"]),
                        "product_type": ProductType.ROASTED_WHOLE_BEAN.value,
                        "discovered_date_time": self.extract_published_date(product),
                        "country_of_origin": (country_of_origin := self.extract_country_of_origin(product["title"], product_details)),
                        "continent": get_continent(country_of_origin),
                        "process": (process := self.extract_process(product_details)),
                        "process_category": self.get_process_category(process),
                        "tasting_notes": self.extract_notes(product["excerpt"], product_details),
                        "varieties": normalize_variety_names(self.extract_varieties(product_details))
                    }

                    variant = product["structuredContent"]["variants"][0]
                    processed_product_variant = {
                        "size": self.extract_size(product["excerpt"]),
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

    def get_product_details(self, product_url):
        response = self.get_with_rate_limiting(product_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        additional_section = soup.find(
            'section', class_="ProductItem-additional")

        if not additional_section:
            return ""

        paragraphs = additional_section.find_all('p')

        combined_text = ' '.join(paragraph.get_text().strip()
                                 for paragraph in paragraphs)

        return combined_text

    def extract_title(self, product):
        title = product["title"]
        last_comma_index = title.rfind(',')

        if last_comma_index != -1:
            return title[:last_comma_index].title()

        return title.title()

    def extract_size(self, excerpt):
        match = re.search(r'\d+g', excerpt)
        if match:
            return parse_size(match.group())
        return 0

    def extract_country_of_origin(self, title, product_details):
        country_from_title = validate_country_name(title)
        return country_from_title if country_from_title != UNKNOWN else validate_country_name(product_details)

    def extract_varieties(self, product_details):
        formatted_product_details = product_details.lower()
        if 'cultivar:' in formatted_product_details:
            varieties = formatted_product_details.split(
                'cultivar:')[1].split('/')[0].strip()
            variety_list = [x.strip().title()
                            for x in re.split(',', varieties)]
            return extract_varieties(' '.join(variety_list))
        return [UNKNOWN]

    def extract_notes(self, excerpt, product_details):
        if 'Tasting Notes:' in product_details:
            notes = product_details.split('Tasting Notes:')[
                1].replace(".", "").strip()
        elif 'Tasting Notes:' in excerpt:
            notes = excerpt.split('Tasting Notes:')[1].replace(
                ".", "").replace("</p>", "").strip()

        notes = notes.replace("&nbsp;", "").strip()

        return [x.strip().title() for x in re.split(',', notes)] if notes else [UNKNOWN]

    def extract_process(self, product_details):
        if 'Process' in product_details:
            process = product_details.split('Process')[1]
            process = process.split(':')[1]
            process = process.split('/')[0]
            if '#' in process:
                process = process.split('#')[0]
            return process.strip().title() if process.strip() else UNKNOWN
        return UNKNOWN

    def build_product_url(self, handle):
        return f"{self.product_base_url}/{handle}"
