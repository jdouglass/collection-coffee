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

get_all_product_to_variety_id_query = """
    SELECT variety_id FROM ProductToVariety WHERE product_id = %s;
"""

get_all_product_to_tasting_note_id_query = """
    SELECT tasting_note_id FROM ProductToTastingNote WHERE product_id = %s;
"""

get_vendor_id_by_vendor_name_query = """
    SELECT id FROM Vendor WHERE name = %s;
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


def get_delete_product_query(format_strings):
    # Generate the formatted query with placeholders
    return f"DELETE FROM Product WHERE vendorId = %s AND productUrl NOT IN ({format_strings});"
