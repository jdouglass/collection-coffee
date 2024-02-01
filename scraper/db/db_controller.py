import MySQLdb
from db.queries import *
from db.db_connection import DBConnection
from utils.supabase_storage_manager import SupabaseStorageManager
from utils.print_once import check_use_database
from config.logger_config import logger
import traceback
from utils.email_notifier import EmailNotifier
from config.config_loader import is_production


class DatabaseController:
    def __init__(self):
        self.connection = None
        self.storage_manager = SupabaseStorageManager()
        self.email_notifier = EmailNotifier()

    def connect(self):
        db_connection = DBConnection()
        self.connection = db_connection.get_connection()

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def update_runtime_timestamp(self, vendor, is_start_time=False):
        cursor = self.connection.cursor()

        try:
            if is_start_time:
                cursor.execute(update_start_time_query, (vendor,))
            else:
                cursor.execute(update_end_time_query, (vendor,))
        except MySQLdb.Error as e:
            if is_start_time:
                logger.debug(
                    f"Error updating the start_time for {vendor}: {e}"
                )
            else:
                logger.debug(
                    f"Error updating the end_time for {vendor}: {e}"
                )
        
        self.connection.commit()
        cursor.close()


    @check_use_database
    def save_to_db(self, products):
        cursor = self.connection.cursor()

        for product in products:
            try:
                cursor.execute(insert_brand_query, (product["brand"],))
            except MySQLdb.Error as e:
                logger.debug(
                    f"Error inserting brand {product['brand']}: {e}")

            cursor.execute(get_product_by_product_url,
                           (product["product_url"],))
            existing_product = cursor.fetchone()

            # Insert product data into Product table
            product_id = None
            try:
                if existing_product:
                    # Update the existing product
                    cursor.execute(update_product_query, (
                        product["brand"],
                        product["country_of_origin"],
                        product["vendor"],
                        product["process_category"],
                        product["product_type"],
                        product["title"],
                        product["process"],
                        product["product_url"],
                        product["discovered_date_time"],
                        product["handle"],
                        product["is_decaf"],
                        # This identifies the record to update
                        product["product_url"]
                    ))
                    product_id = existing_product[0]
                else:
                    # Insert new product
                    cursor.execute(insert_product_query, (
                        product["brand"],
                        product["country_of_origin"],
                        product["vendor"],
                        product["process_category"],
                        product["product_type"],
                        product["title"],
                        product["process"],
                        product["product_url"],
                        self.storage_manager.upload_image(
                            product["image_url"], product["product_url"]),
                        product["discovered_date_time"],
                        product["handle"],
                        product["is_decaf"]
                    ))
                    # After inserting the product, get the product ID
                    cursor.execute(get_product_id_by_product_url_query,
                                   (product["product_url"],))
                    product_id = cursor.fetchone()[0]
            except MySQLdb.Error as e:
                error_message = traceback.format_exc()
                if not is_production:
                    self.email_notifier.send_error_notification(error_message)
                logger.error(
                    f"Error inserting product {product}: {error_message}")
                continue  # skip to the next product

            if not product_id:
                logger.error(
                    "No product ID retrieved or created; skipping variant handling.")

            # Now, handle the ProductVariant information for each product
            # This assumes your variants are within the 'product' object in a 'variants' list
            for variant in product.get("variants", []):
                try:
                    variant_id_exists = 'variant_id' in variant
                    # Check if the variant already exists and update or insert as necessary
                    # You'll need a query to select the variant by some unique identifier, e.g., a combination of product_id and a variant attribute
                    if variant_id_exists:
                        cursor.execute(get_variant_by_identifier_query,
                                       (variant['variant_id'], product_id))
                        existing_variant = cursor.fetchone()

                    if variant_id_exists:
                        if existing_variant:
                            # Update the existing variant entry
                            cursor.execute(update_product_variant_query, (
                                variant["size"],
                                variant["price"],
                                variant["is_sold_out"],
                                variant["variant_id"],
                                product_id,
                            ))
                        else:
                            # Insert new variant entry
                            cursor.execute(insert_product_variant_query, (
                                product_id,
                                variant["variant_id"],
                                variant["size"],
                                variant["price"],
                                variant["is_sold_out"],
                            ))
                    else:
                        if existing_product:
                            # Update the existing variant entry
                            cursor.execute(update_product_variant_without_variant_id_query, (
                                variant["size"],
                                variant["price"],
                                variant["is_sold_out"],
                                product_id,
                            ))
                        else:
                            # Insert new variant entry
                            cursor.execute(insert_product_variant_without_variant_id_query, (
                                product_id,
                                variant["size"],
                                variant["price"],
                                variant["is_sold_out"],
                            ))
                except MySQLdb.Error as e:
                    error_message = traceback.format_exc()
                    if not is_production:
                        self.email_notifier.send_error_notification(
                            error_message)
                    logger.error(
                        f"Error handling product variant {variant}: {error_message}")

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
        select_query = f"SELECT product_url FROM product WHERE vendor_id = %s AND product_url NOT IN ({format_strings});"
        cursor.execute(select_query, [vendor_id] + extracted_urls)
        urls_to_delete = [item[0] for item in cursor.fetchall()]

        # Only after finding the URLs to delete, proceed to delete the variants
        # Step 2: Delete product variants related to products that are going to be deleted
        if urls_to_delete:
            delete_format_strings = ','.join(['%s'] * len(urls_to_delete))

            delete_related_tasting_notes_query = f"DELETE FROM product_to_tasting_note WHERE product_id IN (SELECT id FROM product WHERE product_url IN ({delete_format_strings}));"
            delete_related_varieties_query = f"DELETE FROM product_to_variety WHERE product_id IN (SELECT id FROM product WHERE product_url IN ({delete_format_strings}));"

            cursor.execute(delete_related_tasting_notes_query, urls_to_delete)
            logger.info(
                f"Related tasting notes deleted for {cursor.rowcount} products.")

            cursor.execute(delete_related_varieties_query, urls_to_delete)
            logger.info(
                f"Related varieties deleted for {cursor.rowcount} products.")

            delete_variants_query = f"DELETE FROM product_variant WHERE product_id IN (SELECT id FROM product WHERE product_url IN ({delete_format_strings}));"
            cursor.execute(delete_variants_query, urls_to_delete)
            # Note the number of deleted variants for logging purposes
            deleted_variants_count = cursor.rowcount
            logger.info(f"{deleted_variants_count} product variants deleted.")

        # Step 3: Delete products for the given vendorId that are not in extracted_urls
        delete_query = get_delete_product_query(format_strings)
        cursor.execute(delete_query, [vendor_id] + extracted_urls)
        deleted_count = cursor.rowcount
        logger.info(f"{deleted_count} products deleted")

        self.connection.commit()
        cursor.close()

        # Step 4: Delete the corresponding images from Supabase Storage
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

        cursor.execute(delete_orphaned_tasting_note_relations)
        logger.info(
            f"{cursor.rowcount} orphaned relationships deleted from ProductToTastingNote")

        self.connection.commit()
        cursor.close()
