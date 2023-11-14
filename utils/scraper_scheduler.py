import time
from concurrent.futures import ThreadPoolExecutor
from db.db_controller import DatabaseController
from config.config import PRINT_PRODUCTS, ENABLE_CRON_JOB, USE_DATABASE
from config.logger_config import logger
from apscheduler.schedulers.background import BackgroundScheduler
from utils.email_notifier import EmailNotifier


class ScraperScheduler:
    def __init__(self, scraper_classes):
        self.scraper_classes = scraper_classes
        self.executor = ThreadPoolExecutor(max_workers=len(scraper_classes))
        self.scheduler = BackgroundScheduler()
        self.email_notifier = EmailNotifier()

    def run_scraper(self, vendor):
        start_time = time.time()
        scraper_data = self.scraper_classes.get(vendor)
        if scraper_data is None:
            logger.error(f"No scraper found for vendor: {vendor}")
            return

        logger.debug(f"Starting scraper: {vendor}")
        scraper_class, scraper_url, scraper_mock_data_path, product_base_url = scraper_data
        scraper_instance = scraper_class(
            scraper_url, vendor, scraper_mock_data_path, product_base_url)
        scraper_instance.fetch_products()
        processed_products = scraper_instance.process_products(
            scraper_instance.products)

        if USE_DATABASE:
            db_controller = DatabaseController()
            db_controller.connect()
            db_controller.save_to_db(processed_products)
            db_controller.delete_old_products(processed_products)
            db_controller.delete_orphaned_records()
            db_controller.close_connection()

        if PRINT_PRODUCTS:
            scraper_instance.display_products(processed_products)

        logger.debug(f"Scraper job completed: {vendor}")
        end_time = time.time()
        logger.info(
            f"{vendor} scraper took {end_time - start_time} seconds to finish")

    def run_all_scrapers(self):
        futures = []
        for vendor in self.scraper_classes.keys():
            future = self.executor.submit(self.run_scraper, vendor)
            futures.append(future)

        for future in futures:
            future.result()

    def schedule_scraper(self, vendor=None):
        if vendor:
            logger.info(f"Scheduling scraper for vendor: {vendor}")
            self.scheduler.add_job(
                self.run_scraper, 'interval', minutes=5, args=[vendor])
        else:
            logger.info("Scheduling all scrapers...")
            for vendor in self.scraper_classes.keys():
                self.scheduler.add_job(
                    self.run_scraper, 'interval', minutes=5, args=[vendor])

    def start(self, specific_vendor=None):
        if ENABLE_CRON_JOB:
            self.schedule_scraper(specific_vendor)
            self.scheduler.start()
            try:
                # To keep the main thread alive, otherwise signals are ignored.
                while True:
                    time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                # Not strictly necessary if daemonic mode is enabled but should be done if possible
                self.scheduler.shutdown()
        else:
            if specific_vendor:
                logger.info(
                    "Cron job is disabled. Running the scraper immediately for the specified vendor...")
                self.run_scraper(specific_vendor)
            else:
                logger.info(
                    "Cron job is disabled. Running all scrapers immediately...")
                self.run_all_scrapers()
