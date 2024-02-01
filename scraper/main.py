from config.logger_config import logger
from data.coffee_vendors_data import coffee_vendors_data
from utils.scraper_scheduler import ScraperScheduler
from config.config import ENABLE_CRON_JOB, USE_DATABASE
from config.config_loader import is_production
import argparse

SCRAPER_CLASSES = {
    vendor_data["key"]: (
        vendor_data["scraper_class"],
        vendor_data["url"],
        vendor_data["mock_data_path"],
        vendor_data["product_base_url"],
        vendor_data["home_url"])
    for vendor_data in coffee_vendors_data
}


def confirm_proceed(message):
    response = input(message + " Proceed? (Y/N) ").strip().upper()
    if response != "Y":
        print("Operation cancelled.")
        exit()


def main():
    parser = argparse.ArgumentParser(description='Coffee Scraper')
    parser.add_argument('--vendor', type=str,
                        help='Name of the vendor to scrape', required=False)

    args = parser.parse_args()

    scheduler = ScraperScheduler(SCRAPER_CLASSES)

    if args.vendor:
        scraper_data = SCRAPER_CLASSES.get(args.vendor)

        if scraper_data is None:
            logger.error(f"No scraper found for vendor: {args.vendor}")
            return
        else:
            if ENABLE_CRON_JOB:
                logger.info(
                    "Cron job is enabled. Scheduling the scraper for the specified vendor...")
                scheduler.start(args.vendor)
            else:
                logger.info(
                    "Cron job is disabled. Running the scraper immediately for the specified vendor...")
                scheduler.run_scraper(args.vendor)
    else:
        if ENABLE_CRON_JOB:
            logger.info("Cron job is enabled. Scheduling all scrapers...")
            scheduler.start()
        else:
            logger.info(
                "Cron job is disabled. Running all scrapers immediately...")
            scheduler.run_all_scrapers()


if __name__ == "__main__":
    if USE_DATABASE:
        confirm_proceed("USE_DATABASE feature flag is set to True.")

    print(is_production)

    if is_production:
        confirm_proceed("is_production feature flag is set to True.")

    main()
