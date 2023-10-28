import MySQLdb
from db.queries import *
from db.db_connection import DBConnection
from utils.supabase_storage_manager import SupabaseStorageManager
from utils.print_once import check_use_database
from config.logger_config import logger


class DatabaseController:
    def __init__(self):
        self.connection = None
        self.storage_manager = SupabaseStorageManager()

    def connect(self):
        db_connection = DBConnection()
        self.connection = db_connection.get_connection()

    def close_connection(self):
        if self.connection:
            self.connection.close()

    @check_use_database
    def save_to_db(self, products):
        cursor = self.connection.cursor()

        for product in products:
            try:
                cursor.execute(insert_brand_query, (product["brand"],))
            except MySQLdb.Error as e:
                logger.debug(
                    f"Error inserting brand {product['brand']}: {e}")

            # Upload image to Supabase bucket
            bucket_image_list = self.storage_manager.get_storage_list()
            uploaded_image_url = self.storage_manager.upload_image(
                product["image_url"], product["product_url"], bucket_image_list)

            # Insert product data into Product table
            try:
                cursor.execute(insert_product_query, (
                    product["brand"],
                    product["country_of_origin"],
                    product["vendor"],
                    product["process_category"],
                    product["product_type"],
                    product["title"],
                    product["weight"],
                    product["process"],
                    product["product_url"],
                    uploaded_image_url,
                    product["is_sold_out"],
                    product["discovered_date_time"],
                    product["handle"],
                    product["price"],
                    product["is_decaf"]
                ))
            except MySQLdb.Error as e:
                logger.error(
                    f"Error inserting product {product}: {e}")

            # Insert the product first to get the product ID
            cursor.execute(get_product_id_query, (product["product_url"],))
            result = cursor.fetchone()
            if result:
                product_id = result[0]
            else:
                logger.info(
                    "No results found for the given product URL.")
                continue  # skip this iteration and move to the next product

            # For varieties
            existing_varieties = set()
            cursor.execute(
                get_all_product_to_variety_id_query, (product_id,))
            for row in cursor.fetchall():
                existing_varieties.add(row[0])

            scraped_varieties = set()
            for variety in product.get("varieties", []):
                cursor.execute(insert_variety_query, (variety,))
                cursor.execute(get_variety_id_query, (variety,))
                variety_id = cursor.fetchone()[0]
                scraped_varieties.add(variety_id)

                # Insert new relationships
                if variety_id not in existing_varieties:
                    cursor.execute(insert_product_to_variety_query,
                                   (product_id, variety_id))

            # Remove old relationships
            for old_variety in existing_varieties - scraped_varieties:
                cursor.execute(delete_product_to_variety_query,
                               (product_id, old_variety))

            # For tasting notes
            existing_tasting_notes = set()
            cursor.execute(
                get_all_product_to_tasting_note_id_query, (product_id,))
            for row in cursor.fetchall():
                existing_tasting_notes.add(row[0])

            scraped_tasting_notes = set()
            for tasting_note in product.get("tasting_notes", []):
                cursor.execute(insert_tasting_note_query, (tasting_note,))
                cursor.execute(get_tasting_note_id_query, (tasting_note,))
                tasting_note_id = cursor.fetchone()[0]
                scraped_tasting_notes.add(tasting_note_id)

                # Insert new relationships
                if tasting_note_id not in existing_tasting_notes:
                    cursor.execute(insert_product_to_tasting_note_query,
                                   (product_id, tasting_note_id))

            # Remove old relationships
            for old_tasting_note in existing_tasting_notes - scraped_tasting_notes:
                cursor.execute(delete_product_to_tasting_note_query,
                               (product_id, old_tasting_note))

        self.connection.commit()
        cursor.close()

    @check_use_database
    def delete_old_products(self, products):
        cursor = self.connection.cursor()

        extracted_urls = [product["product_url"] for product in products]

        # Fetch vendorId based on vendor's name
        cursor.execute(get_vendor_id_by_vendor_name_query,
                       (products[0]["vendor"],))
        vendor_id = cursor.fetchone()
        if vendor_id is None:
            logger.debug("Vendor not found in the database!")
            return
        vendor_id = vendor_id[0]

        # Step 1: Fetch the product URLs of the products that are about to be deleted
        format_strings = ','.join(['%s'] * len(extracted_urls))
        select_query = f"SELECT productUrl FROM Product WHERE vendorId = %s AND productUrl NOT IN ({format_strings});"
        cursor.execute(select_query, [vendor_id] + extracted_urls)
        urls_to_delete = [item[0] for item in cursor.fetchall()]

        # Step 2: Delete products for the given vendorId that are not in extracted_urls
        delete_query = get_delete_product_query(format_strings)
        cursor.execute(delete_query, [vendor_id] + extracted_urls)
        deleted_count = cursor.rowcount
        logger.info(f"{deleted_count} products deleted")

        self.connection.commit()
        cursor.close()

        # Step 3: Delete the corresponding images from Supabase Storage
        storage_manager = SupabaseStorageManager()
        for url in urls_to_delete:
            storage_manager.delete_image(url)
            logger.info(f"Image for product URL {url} requested to be deleted")

    @check_use_database
    def delete_orphaned_records(self):
        cursor = self.connection.cursor()

        cursor.execute(delete_orphaned_brands_query)
        logger.info(f"{cursor.rowcount} orphan brands deleted")

        cursor.execute(delete_orphaned_tasting_notes_query)
        logger.info(f"{cursor.rowcount} orphan tasting notes deleted")

        cursor.execute(delete_orphaned_varieties_query)
        logger.info(f"{cursor.rowcount} orphan varieties deleted")

        cursor.execute(delete_orphaned_variety_relations)
        logger.info(
            f"{cursor.rowcount} orphaned relationships deleted from ProductToVariety")

        cursor.execute(delete_orphaned_variety_relations)
        logger.info(
            f"{cursor.rowcount} orphaned relationships deleted from ProductToTastingNote")

        self.connection.commit()
        cursor.close()
