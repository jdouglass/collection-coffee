import MySQLdb
import os
from dotenv import load_dotenv
from config.constants import LOG_FILENAME
from utils.print_once import check_use_database
from config.logger_config import logger
load_dotenv()

# Retrieve database configuration from environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USERNAME')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')


def get_db_connection():
    connection = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASS,
        db=DB_NAME,
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "./config/cacert.pem"
        }
    )
    return connection


@check_use_database
def save_to_db(products):

    connection = get_db_connection()
    cursor = connection.cursor()

    insert_variety_query = """
        INSERT IGNORE INTO Variety (name) VALUES (%s)
    """

    insert_tasting_note_query = """
        INSERT IGNORE INTO TastingNote (name) VALUES (%s)
    """

    insert_brand_query = """
        INSERT IGNORE INTO Brand (name) VALUES (%s)
    """

    insert_product_query = """
        INSERT INTO Product (
        brandId, 
        countryOfOriginId, 
        vendorId, 
        processCategoryId, 
        productTypeId, 
        title, 
        weight, 
        process, 
        productUrl, 
        imageUrl, 
        soldOut, 
        discoveredDateTime, 
        handle, 
        price, 
        decaf
    ) 
    VALUES (
        (SELECT id FROM Brand WHERE name = %s),
        (SELECT id FROM Country WHERE name = %s),
        (SELECT id FROM Vendor WHERE name = %s),
        (SELECT id FROM ProcessCategory WHERE name = %s),
        (SELECT id FROM ProductType WHERE name = %s),
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    )
    ON DUPLICATE KEY UPDATE 
        brandId = VALUES(brandId),
        countryOfOriginId = VALUES(countryOfOriginId),
        vendorId = VALUES(vendorId),
        processCategoryId = VALUES(processCategoryId),
        productTypeId = VALUES(productTypeId),
        title = VALUES(title),
        weight = VALUES(weight),
        process = VALUES(process),
        imageUrl = VALUES(imageUrl),
        soldOut = VALUES(soldOut),
        discoveredDateTime = VALUES(discoveredDateTime),
        handle = VALUES(handle),
        price = VALUES(price),
        decaf = VALUES(decaf);
    """

    get_product_id_query = """
        SELECT id FROM Product WHERE productUrl = %s;
    """

    insert_product_to_variety_query = """
        INSERT IGNORE INTO ProductToVariety (product_id, variety_id) VALUES (%s, %s);
    """

    insert_product_to_tasting_note_query = """
        INSERT IGNORE INTO ProductToTastingNote (product_id, tasting_note_id) VALUES (%s, %s);
    """

    get_variety_id_query = """
        SELECT id FROM Variety WHERE name = %s;
    """

    get_tasting_note_id_query = """
        SELECT id FROM TastingNote WHERE name = %s;
    """

    delete_product_to_variety_query = """
        DELETE FROM ProductToVariety WHERE product_id = %s AND variety_id = %s;
    """

    delete_product_to_tasting_note_query = """
        DELETE FROM ProductToTastingNote WHERE product_id = %s AND tasting_note_id = %s;
    """

    for product in products:
        try:
            cursor.execute(insert_brand_query, (product["brand"],))
        except MySQLdb.Error as e:
            logger.debug(
                f"Duplicate brand not inserted {product['brand']}: {e}")

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
                product["image_url"],
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
            "SELECT variety_id FROM ProductToVariety WHERE product_id = %s;", (product_id,))
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
            "SELECT tasting_note_id FROM ProductToTastingNote WHERE product_id = %s;", (product_id,))
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

    connection.commit()
    cursor.close()
    connection.close()


@check_use_database
def delete_old_products(products):
    connection = get_db_connection()
    cursor = connection.cursor()

    extracted_urls = [product["product_url"] for product in products]

    # Fetch vendorId based on vendor's name
    cursor.execute("SELECT id FROM Vendor WHERE name = %s;",
                   (products[0]["vendor"],))
    vendor_id = cursor.fetchone()
    if vendor_id is None:
        logger.debug("Vendor not found in the database!")
        return
    vendor_id = vendor_id[0]  # Extracting ID from the tuple

    # Delete products for the given vendorId that are not in extracted_urls
    format_strings = ','.join(['%s'] * len(extracted_urls))
    delete_query = f"DELETE FROM Product WHERE vendorId = %s AND productUrl NOT IN ({format_strings});"
    cursor.execute(delete_query, [vendor_id] + extracted_urls)
    logger.info(f"{cursor.rowcount} products deleted")

    connection.commit()
    cursor.close()
    connection.close()


@check_use_database
def delete_orphaned_records():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete brands with no relations in Product table
    delete_orphaned_brands_query = """
    DELETE brands
    FROM Brand brands
    LEFT JOIN Product products ON brands.id = products.brandId
    WHERE products.id IS NULL;
    """

    cursor.execute(delete_orphaned_brands_query)
    logger.info(f"{cursor.rowcount} orphan brands deleted")

    # Deleting orphaned tasting notes
    delete_orphaned_tasting_notes_query = """
        DELETE FROM TastingNote
        WHERE id NOT IN (
            SELECT DISTINCT tasting_note_id FROM ProductToTastingNote
        );
    """
    cursor.execute(delete_orphaned_tasting_notes_query)
    logger.info(f"{cursor.rowcount} orphan tasting notes deleted")

    # Deleting orphaned varieties
    delete_orphaned_varieties_query = """
        DELETE FROM Variety
        WHERE id NOT IN (
            SELECT DISTINCT variety_id FROM ProductToVariety
        );
    """
    cursor.execute(delete_orphaned_varieties_query)
    logger.info(f"{cursor.rowcount} orphan varieties deleted")

    # Deleting orphaned relationships in ProductToVariety and ProductToTastingNote
    cursor.execute('''
        DELETE FROM ProductToVariety
        WHERE product_id NOT IN (SELECT id FROM Product)
    ''')
    logger.info(
        f"{cursor.rowcount} orphaned relationships deleted from ProductToVariety")

    cursor.execute('''
        DELETE FROM ProductToTastingNote
        WHERE product_id NOT IN (SELECT id FROM Product)
    ''')
    logger.info(
        f"{cursor.rowcount} orphaned relationships deleted from ProductToTastingNote")

    connection.commit()
    cursor.close()
    connection.close()
