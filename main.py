import argparse
from scrapers.vendor.traffic_coffee_scraper import TrafficCoffeeScraper
from db.db_manager import save_to_db, delete_old_products, delete_orphaned_records

SCRAPER_CLASSES = {
    "Traffic Coffee": (TrafficCoffeeScraper, "https://www.trafficcoffee.com/collections/our-coffees/products.json?limit=250")
    # You can extend this by adding more vendor: (ScraperClass, URL) pairs
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Coffee Scraper')
    parser.add_argument('vendor', type=str,
                        help='Name of the vendor to scrape')

    args = parser.parse_args()

    scraper_data = SCRAPER_CLASSES.get(args.vendor)

    if scraper_data is None:
        print(f"No scraper found for vendor: {args.vendor}")
    else:
        scraper_class, scraper_url = scraper_data
        scraper_instance = scraper_class(scraper_url, args.vendor)
        scraper_instance.fetch_products()
        processed_products = scraper_instance.process_products(
            scraper_instance.products)
        save_to_db(processed_products)
        delete_old_products(processed_products)
        delete_orphaned_records()
        # scraper_instance.display_products(processed_products)
