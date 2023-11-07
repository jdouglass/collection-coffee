insert_variety_query = """
        INSERT IGNORE INTO Variety (name) VALUES (%s)
    """

insert_tasting_note_query = """
    INSERT IGNORE INTO TastingNote (name) VALUES (%s)
"""

insert_brand_query = """
    INSERT IGNORE INTO Brand (name) VALUES (%s)
"""

insert_vendor_query = """
    INSERT IGNORE INTO Vendor (name) VALUES (%s)
"""

insert_product_query = """
    INSERT INTO Product (
    brandId, 
    countryOfOriginId, 
    vendorId, 
    processCategoryId, 
    productTypeId, 
    title, 
    process, 
    productUrl, 
    imageUrl, 
    discoveredDateTime, 
    handle, 
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
    %s
)
"""

update_product_query = """
    UPDATE Product
    SET
        brandId = (SELECT id FROM Brand WHERE name = %s),
        countryOfOriginId = (SELECT id FROM Country WHERE name = %s),
        vendorId = (SELECT id FROM Vendor WHERE name = %s),
        processCategoryId = (SELECT id FROM ProcessCategory WHERE name = %s),
        productTypeId = (SELECT id FROM ProductType WHERE name = %s),
        title = %s,
        process = %s,
        productUrl = %s,
        discoveredDateTime = %s,
        handle = %s,
        decaf = %s
    WHERE
        productUrl = %s;
"""

insert_product_variant_query = """
    INSERT INTO ProductVariant (
        productId, 
        variantId, 
        size, 
        price, 
        soldOut
    )
    VALUES (
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    )
"""

update_product_variant_query = """
    UPDATE ProductVariant
    SET size = %s, price = %s, soldOut = %s
    WHERE variantId = %s AND productId = %s
"""

get_variant_by_identifier_query = """
    SELECT id FROM ProductVariant WHERE variantId = %s AND productId = %s;
"""

delete_variants_query = """
    DELETE ProductVariant FROM ProductVariant
    JOIN Product ON ProductVariant.productId = Product.id
    WHERE Product.productUrl IN (%s)
"""

get_product_id_by_product_url_query = """
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

get_all_product_to_variety_id_query = """
    SELECT variety_id FROM ProductToVariety WHERE product_id = %s;
"""

get_all_product_to_tasting_note_id_query = """
    SELECT tasting_note_id FROM ProductToTastingNote WHERE product_id = %s;
"""

get_vendor_id_by_vendor_name_query = """
    SELECT id FROM Vendor WHERE name = %s;
"""

get_image_url_by_product_url_query = """
    SELECT imageUrl FROM Product WHERE productUrl = %s;
"""

get_product_by_product_url = """
    SELECT * FROM Product WHERE productUrl = %s;
"""

delete_orphaned_brands_query = """
    DELETE brands
    FROM Brand brands
    LEFT JOIN Product products ON brands.id = products.brandId
    WHERE products.id IS NULL;
"""

delete_orphaned_tasting_notes_query = """
    DELETE FROM TastingNote
    WHERE id NOT IN (
        SELECT DISTINCT tasting_note_id FROM ProductToTastingNote
    );
"""

delete_orphaned_varieties_query = """
    DELETE FROM Variety
    WHERE id NOT IN (
        SELECT DISTINCT variety_id FROM ProductToVariety
    );
"""

delete_orphaned_variety_relations = """
    DELETE FROM ProductToVariety
    WHERE product_id NOT IN (SELECT id FROM Product)
"""

delete_orphaned_tasting_note_relations = """
    DELETE FROM ProductToTastingNote
    WHERE product_id NOT IN (SELECT id FROM Product)
"""

insert_continent_query = """
    INSERT INTO Continent (name) VALUES (%s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
"""

insert_country_query = """
    INSERT INTO Country (name, continentId) VALUES (%s, (SELECT id FROM Continent WHERE name = %s))
"""

insert_currency_code_query = """
    INSERT INTO CurrencyCode (code) VALUES (%s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
"""

insert_vendor_query = """
    INSERT INTO Vendor (
        name, 
        countryId, 
        currencyCodeId
    ) VALUES (%s, (SELECT id FROM Country WHERE name = %s), (SELECT id FROM CurrencyCode WHERE code = %s))
"""

seed_vendor_query = """
    INSERT INTO Vendor (name, countryId, currencyCodeId)
    VALUES (%s, %s, %s)
"""

seed_process_category_query = """
    INSERT INTO ProcessCategory (name)
    VALUES (%s)
"""

seed_product_type_query = """
    INSERT INTO ProductType (name)
    VALUES (%s)
"""

get_id_by_country_name_query = "SELECT id FROM Country WHERE name = %s"

get_id_by_currency_code_query = "SELECT id FROM CurrencyCode WHERE code = %s"

get_id_by_process_category_name_query = "SELECT id FROM ProcessCategory WHERE name = %s;"

get_id_by_product_type_name_query = "SELECT id FROM ProductType WHERE name = %s;"


def get_delete_product_query(format_strings):
    # Generate the formatted query with placeholders
    return f"DELETE FROM Product WHERE vendorId = %s AND productUrl NOT IN ({format_strings});"
