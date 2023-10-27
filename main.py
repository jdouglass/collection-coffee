import argparse
from db.db_controller import DatabaseController
from data.coffee_vendors_data import coffee_vendors_data
from config.config import PRINT_PRODUCTS
from config.logger_config import logger

SCRAPER_CLASSES = {
    vendor_data["key"]: (
        vendor_data["scraper_class"], vendor_data["url"], vendor_data["mock_data_path"])
    for vendor_data in coffee_vendors_data
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Coffee Scraper')
    parser.add_argument('vendor', type=str,
                        help='Name of the vendor to scrape')

    args = parser.parse_args()

    scraper_data = SCRAPER_CLASSES.get(args.vendor)

    if scraper_data is None:
        logger.error(f"No scraper found for vendor: {args.vendor}")
    else:
        scraper_class, scraper_url, scraper_mock_data_path = scraper_data
        scraper_instance = scraper_class(
            scraper_url, args.vendor, scraper_mock_data_path)
        scraper_instance.fetch_products()
        processed_products = scraper_instance.process_products(
            scraper_instance.products)

        db_controller = DatabaseController()
        db_controller.connect()
        db_controller.save_to_db(processed_products)
        db_controller.delete_old_products(processed_products)
        db_controller.delete_orphaned_records()
        db_controller.close_connection()

        if PRINT_PRODUCTS:
            scraper_instance.display_products(processed_products)
