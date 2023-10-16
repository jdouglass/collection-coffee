import MySQLdb
import os
from config.config import USE_DATABASE
from dotenv import load_dotenv

from utils.print_once import check_use_database
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

    check_product_to_variety_query = """
        SELECT COUNT(*)
        FROM ProductToVariety
        WHERE product_id = %s AND variety_id = %s;
    """

    check_product_to_tasting_note_query = """
        SELECT COUNT(*)
        FROM ProductToTastingNote
        WHERE product_id = %s AND tasting_note_id = %s;
    """

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

    for product in products:
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
            print(f"Error inserting product {product['title']}: {e}")

        # Insert the product first to get the product ID
        cursor.execute(get_product_id_query, (product["product_url"],))
        product_id = cursor.fetchone()[0]

        varieties = product.get("varieties", [])
        tasting_notes = product.get("tasting_notes", [])

        try:
            cursor.execute(insert_brand_query, (product["brand"],))
        except MySQLdb.Error as e:
            print(f"Duplicate brand not inserted {product['brand']}: {e}")

        for variety in varieties:
            cursor.execute(insert_variety_query, (variety,))
            cursor.execute(get_variety_id_query, (variety,))
            variety_id = cursor.fetchone()[0]

            # Check if the relationship already exists
            cursor.execute(check_product_to_variety_query,
                           (product_id, variety_id))
            if cursor.fetchone()[0] == 0:  # Relationship doesn't exist
                cursor.execute(insert_product_to_variety_query,
                               (product_id, variety_id))

        for tasting_note in tasting_notes:
            cursor.execute(insert_tasting_note_query, (tasting_note,))
            cursor.execute(get_tasting_note_id_query, (tasting_note,))
            tasting_note_id = cursor.fetchone()[0]

            # Check if the relationship already exists
            cursor.execute(check_product_to_tasting_note_query,
                           (product_id, tasting_note_id))
            if cursor.fetchone()[0] == 0:  # Relationship doesn't exist
                cursor.execute(insert_product_to_tasting_note_query,
                               (product_id, tasting_note_id))

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
        print("Vendor not found in the database!")
        return
    vendor_id = vendor_id[0]  # Extracting ID from the tuple

    # Delete products for the given vendorId that are not in extracted_urls
    format_strings = ','.join(['%s'] * len(extracted_urls))
    delete_query = f"DELETE FROM Product WHERE vendorId = %s AND productUrl NOT IN ({format_strings});"
    cursor.execute(delete_query, [vendor_id] + extracted_urls)
    print(f"{cursor.rowcount} products deleted")

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
    print(f"{cursor.rowcount} orphan brands deleted")

    # Deleting orphaned tasting notes
    delete_orphaned_tasting_notes_query = """
        DELETE FROM TastingNote
        WHERE id NOT IN (
            SELECT DISTINCT tasting_note_id FROM ProductToTastingNote
        );
    """
    cursor.execute(delete_orphaned_tasting_notes_query)
    print(f"{cursor.rowcount} orphan tasting notes deleted")

    # Deleting orphaned varieties
    delete_orphaned_varieties_query = """
        DELETE FROM Variety
        WHERE id NOT IN (
            SELECT DISTINCT variety_id FROM ProductToVariety
        );
    """
    cursor.execute(delete_orphaned_varieties_query)
    print(f"{cursor.rowcount} orphan varieties deleted")

    # Deleting orphaned relationships in ProductToVariety and ProductToTastingNote
    cursor.execute('''
        DELETE FROM ProductToVariety
        WHERE product_id NOT IN (SELECT id FROM Product)
    ''')
    print(f"{cursor.rowcount} orphaned relationships deleted from ProductToVariety")

    cursor.execute('''
        DELETE FROM ProductToTastingNote
        WHERE product_id NOT IN (SELECT id FROM Product)
    ''')
    print(f"{cursor.rowcount} orphaned relationships deleted from ProductToTastingNote")

    connection.commit()
    cursor.close()
    connection.close()
