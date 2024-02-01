from helpers.country_to_continent_mapper import get_continent
from helpers.variety_normalizer import normalize_variety_names
from config.constants import UNKNOWN, DEFAULT_IMAGE_URL
from config.logger_config import logger
from helpers.size_parser import parse_size
from helpers.country_name_validator import validate_country_name
from enums.product_type import ProductType
from helpers.variety_extractor import extract_varieties
import re
import traceback
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from helpers.title_formatter import title_formatter
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from utils.error_handler import handle_exception
from scrapers.base.base_scraper import BaseScraper
import logging


class HatchCoffeeRoasterScraper(BaseScraper):
    def __init__(self, url, vendor, mock_data_path, product_base_url, home_url):
        super().__init__(url, vendor, mock_data_path, product_base_url, home_url)

    def process_products(self, fetched_products):
        processed_products = []
        for url in fetched_products:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = self.extract_title(soup)
            if not any(word in title.lower() for word in self.excluded_words):
                body_content = self.extract_body_content(soup)

                try:
                    processed_product_variants = []
                    processed_product = {
                        "brand": self.vendor,
                        "vendor": self.vendor,
                        "title": title,
                        "handle": self.extract_handle(url),
                        "product_url": url,
                        "image_url": self.extract_image_url(soup),
                        "is_decaf": self.is_decaf(title),
                        "product_type": self.extract_product_type(body_content),
                        "discovered_date_time": datetime.now(),
                        "country_of_origin": (country_of_origin := self.extract_country_of_origin(body_content)),
                        "continent": get_continent(country_of_origin),
                        "process": (process := self.extract_process(body_content)),
                        "process_category": self.get_process_category(process),
                        "tasting_notes": self.extract_notes(body_content),
                        "varieties": normalize_variety_names(self.extract_varieties(body_content)),
                    }

                    select_tag = soup.find('select', {'name': 'variants'})

                    if select_tag:
                        options_tags = select_tag.find_all('option')

                        for option in options_tags:
                            if option.get('value') != "-1":
                                option_data = {
                                    'variant_id': int(option.get('value')),
                                    'size': parse_size(option.text.strip()),
                                    'price': round(Decimal(option.get('data-price').split('$')[-1].strip()), 2),
                                    'is_sold_out': True if 'unavailable' in option.get('data-stock').strip().lower() else False,
                                }
                                processed_product_variants.append(option_data)
                    else:
                        option_data = {
                            'size': self.extract_size(body_content),
                            'price': self.extract_price(soup),
                            'is_sold_out': self.is_sold_out(soup),
                        }
                        processed_product_variants.append(option_data)

                    processed_product["variants"] = processed_product_variants
                    processed_products.append(processed_product)
                except Exception as e:
                    handle_exception(e, context_info=f"Error processing product from vendor: {self.vendor}")

        return processed_products

    def extract_body_content(self, soup: BeautifulSoup):
        description_div = soup.find("div", class_="product-item-description")

        if not description_div:
            return []

        # Extract text from each <p> tag, split by lines, and filter out empty strings
        description_lines = []
        for p_tag in description_div.find_all("p"):
            lines = p_tag.get_text(separator="\n").split("\n")
            description_lines.extend(
                filter(None, [line.strip() for line in lines]))

        return description_lines

    def extract_price(self, soup: BeautifulSoup):
        return round(Decimal(soup.find('span', class_="product-item-price").get_text().split("$")[-1].strip()), 2)

    def is_sold_out(self, soup: BeautifulSoup):
        return True if 'unavailable' in soup.find('span', class_="helper-tooltip-stock").get_text().strip().lower() else False

    def extract_title(self, soup: BeautifulSoup):
        return soup.find('div', class_="product-item-title").get_text().strip()

    def extract_handle(self, product_url):
        return product_url.split('/')[-1]

    def extract_product_type(self, body_content: list):
        for content in body_content:
            if ProductType.INSTANT.value.lower() in content.lower():
                return ProductType.INSTANT.value
        return ProductType.ROASTED_WHOLE_BEAN.value

    def extract_image_url(self, soup: BeautifulSoup):
        product_image_div = soup.find("div", class_="product-item-image")

        if product_image_div:
            img_tag = product_image_div.find("img")
            if img_tag and 'src' in img_tag.attrs:
                return img_tag['src']
        return DEFAULT_IMAGE_URL

    def extract_country_of_origin(self, body_content: list):
        origin_keywords = ["Origin:", "Origins:"]
        for i, content in enumerate(body_content):
            if any(keyword in content for keyword in origin_keywords):
                if i + 1 < len(body_content):
                    next_content = body_content[i + 1]
                    return validate_country_name(next_content.strip())
        return UNKNOWN

    def extract_varieties(self, body_content: list):
        for content in body_content:
            if 'Variety:' in content:
                variety_info = content.split("Variety:")[-1].strip().title()
                if variety_info:
                    variety_list = [x.strip().title()
                                    for x in re.split(',', variety_info)]
                    return extract_varieties(' '.join(variety_list))
                return [UNKNOWN]
        return [UNKNOWN]

    def extract_notes(self, body_content):
        for i, content in enumerate(body_content):
            if 'Notes:' in content:
                if i + 1 < len(body_content):
                    notes_content = body_content[i + 1]
                    if notes_content:
                        return [title_formatter(x.strip())
                                for x in re.split(',', notes_content)]
                    return [UNKNOWN]
        return [UNKNOWN]

    def extract_process(self, body_content: list):
        for content in body_content:
            if 'Process:' in content:
                return content.split("Process:")[-1].strip().title()
        return UNKNOWN

    def extract_size(self, body_content: list):
        search_patterns = {
            'kg': r'\d+kg',
            'g': r'\d+g',
            'grams': r'\d+ grams'
        }
        for i, content in enumerate(body_content):
            if 'Order details:' in content:
                if i + 1 < len(body_content):
                    price_content = body_content[i + 1]
                    if price_content:
                        for pattern in search_patterns.values():
                            match = re.search(pattern, price_content)
                            if match:
                                return parse_size(match.group())
        for pattern in search_patterns.values():
            for content in body_content:
                match = re.search(pattern, content)
                if match:
                    return parse_size(match.group())
        return 0

    def build_product_url(self, handle):
        return f"{self.product_base_url}{handle}"

    def fetch_products(self):
        product_urls = []

        selenium_logger = logging.getLogger(
            'selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARNING)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.get(f"{self.home_url}/shop")

        while True:
            try:
                load_more_buttons = driver.find_elements(By.LINK_TEXT,
                                                         "Load More")
                if not load_more_buttons:
                    break

                load_more_buttons[0].click()
                time.sleep(2)

            except Exception as e:
                handle_exception(e, context_info=f"Error processing product from vendor: {self.vendor}\n{self.build_product_url(handle)}")
                break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Find all 'product-image-block' and extract 'href' from nested <a> tags
        for block in soup.find_all("div", class_="product-image-block"):
            a_tag = block.find("a")
            if a_tag and 'href' in a_tag.attrs:
                product_url = a_tag['href']
                if product_url not in product_urls and '/shop/' in product_url:
                    product_urls.append(product_url)

        driver.quit()

        self.products = product_urls
