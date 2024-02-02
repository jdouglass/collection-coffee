update_start_time_query = """
    UPDATE runtime
    SET start_time = CURRENT_TIMESTAMP
    FROM (SELECT id FROM vendor WHERE name = %s) AS vendor
    WHERE runtime.vendor_id = vendor.id
"""

update_end_time_query = """
    UPDATE runtime
    SET end_time = CURRENT_TIMESTAMP
    FROM (SELECT id FROM vendor WHERE name = %s) AS vendor
    WHERE runtime.vendor_id = vendor.id
"""

insert_variety_query = """
    INSERT INTO variety (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;
"""

insert_tasting_note_query = """
    INSERT INTO tasting_note (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;
"""

insert_brand_query = """
    INSERT INTO brand (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;
"""

insert_vendor_query = """
    INSERT INTO vendor (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;
"""

insert_product_query = """
    INSERT INTO product (
    brand_id, 
    country_of_origin_id, 
    vendor_id, 
    process_category_id, 
    product_type_id, 
    title, 
    process, 
    product_url, 
    image_url, 
    discovered_date_time, 
    product_handle, 
    is_decaf
) 
VALUES (
    (SELECT id FROM brand WHERE name = %s),
    (SELECT id FROM country WHERE name = %s),
    (SELECT id FROM vendor WHERE name = %s),
    (SELECT id FROM process_category WHERE name = %s),
    (SELECT id FROM product_type WHERE name = %s),
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
    UPDATE product
    SET
        brand_id = (SELECT id FROM brand WHERE name = %s),
        country_of_origin_id = (SELECT id FROM country WHERE name = %s),
        vendor_id = (SELECT id FROM vendor WHERE name = %s),
        process_category_id = (SELECT id FROM process_category WHERE name = %s),
        product_type_id = (SELECT id FROM product_type WHERE name = %s),
        title = %s,
        process = %s,
        product_url = %s,
        discovered_date_time = %s,
        product_handle = %s,
        is_decaf = %s
    WHERE
        product_url = %s;
"""

update_product_without_date_time_query = """
    UPDATE product
    SET
        brand_id = (SELECT id FROM brand WHERE name = %s),
        country_of_origin_id = (SELECT id FROM country WHERE name = %s),
        vendor_id = (SELECT id FROM vendor WHERE name = %s),
        process_category_id = (SELECT id FROM process_category WHERE name = %s),
        product_type_id = (SELECT id FROM product_type WHERE name = %s),
        title = %s,
        process = %s,
        product_url = %s,
        product_handle = %s,
        is_decaf = %s
    WHERE
        product_url = %s;
"""

insert_product_variant_query = """
    INSERT INTO product_variant (
        product_id, 
        variant_id, 
        product_size, 
        product_price, 
        is_sold_out
    )
    VALUES (
        %s, 
        %s, 
        %s, 
        %s, 
        %s
    )
"""

insert_product_variant_without_variant_id_query = """
    INSERT INTO product_variant (
        product_id, 
        product_size, 
        product_price, 
        is_sold_out
    )
    VALUES (
        %s, 
        %s, 
        %s, 
        %s
    )
"""

update_product_variant_query = """
    UPDATE product_variant
    SET product_size = %s, product_price = %s, is_sold_out = %s
    WHERE variant_id = %s AND product_id = %s
"""

update_product_variant_without_variant_id_query = """
    UPDATE product_variant
    SET product_size = %s, product_price = %s, is_sold_out = %s
    WHERE product_id = %s
"""

get_variant_by_identifier_query = """
    SELECT id FROM product_variant WHERE variant_id = %s AND product_id = %s;
"""

delete_variants_query = """
    DELETE product_variant FROM product_variant
    JOIN product ON product_variant.product_id = product.id
    WHERE product.product_url IN (%s)
"""

get_product_id_by_product_url_query = """
    SELECT id FROM product WHERE product_url = %s;
"""

insert_product_to_variety_query = """
    INSERT INTO product_to_variety (product_id, variety_id) VALUES (%s, %s);
"""

insert_product_to_tasting_note_query = """
    INSERT INTO product_to_tasting_note (product_id, tasting_note_id) VALUES (%s, %s);
"""

get_variety_id_query = """
    SELECT id FROM variety WHERE name = %s;
"""

get_tasting_note_id_query = """
    SELECT id FROM tasting_note WHERE name = %s;
"""

delete_product_to_variety_query = """
    DELETE FROM product_to_variety WHERE product_id = %s AND variety_id = %s;
"""

delete_product_to_tasting_note_query = """
    DELETE FROM product_to_tasting_note WHERE product_id = %s AND tasting_note_id = %s;
"""

get_all_product_to_variety_id_query = """
    SELECT variety_id FROM product_to_variety WHERE product_id = %s;
"""

get_all_product_to_tasting_note_id_query = """
    SELECT tasting_note_id FROM product_to_tasting_note WHERE product_id = %s;
"""

get_vendor_id_by_vendor_name_query = """
    SELECT id FROM vendor WHERE name = %s;
"""

get_image_url_by_product_url_query = """
    SELECT image_url FROM product WHERE product_url = %s;
"""

get_product_by_product_url = """
    SELECT * FROM product WHERE product_url = %s;
"""

delete_orphaned_brands_query = """
    DELETE FROM brand
    USING product
    WHERE brand.id = product.brand_id
    AND product.id IS NULL;
"""

delete_orphaned_tasting_notes_query = """
    DELETE FROM tasting_note
    WHERE id NOT IN (
        SELECT DISTINCT tasting_note_id FROM product_to_tasting_note
    );
"""

delete_orphaned_varieties_query = """
    DELETE FROM variety
    WHERE id NOT IN (
        SELECT DISTINCT variety_id FROM product_to_variety
    );
"""

delete_orphaned_variety_relations = """
    DELETE FROM product_to_variety
    WHERE product_id NOT IN (SELECT id FROM product)
"""

delete_orphaned_tasting_note_relations = """
    DELETE FROM product_to_tasting_note
    WHERE product_id NOT IN (SELECT id FROM product)
"""

insert_continent_query = """
    INSERT INTO continent (name) VALUES (%s) ON CONFLICT (name) DO NOTHING
"""

insert_country_query = """
    INSERT INTO country (name, continentId) VALUES (%s, (SELECT id FROM continent WHERE name = %s))
"""

insert_currency_code_query = """
    INSERT INTO currency_code (code) VALUES (%s) ON CONFLICT (name) DO NOTHING
"""

insert_vendor_query = """
    INSERT INTO vendor (
        name, 
        countryId, 
        currencyCodeId
    ) VALUES (%s, (SELECT id FROM country WHERE name = %s), (SELECT id FROM currency_code WHERE code = %s))
"""

seed_vendor_query = """
    INSERT INTO vendor (name, countryId, currencyCodeId)
    VALUES (%s, %s, %s)
"""

seed_process_category_query = """
    INSERT INTO process_category (name)
    VALUES (%s)
"""

seed_product_type_query = """
    INSERT INTO product_type (name)
    VALUES (%s)
"""

get_id_by_country_name_query = "SELECT id FROM country WHERE name = %s"

get_id_by_currency_code_query = "SELECT id FROM currency_code WHERE code = %s"

get_id_by_process_category_name_query = "SELECT id FROM process_category WHERE name = %s;"

get_id_by_product_type_name_query = "SELECT id FROM productType WHERE name = %s;"


def get_delete_product_query(format_strings):
    # Generate the formatted query with placeholders
    return f"DELETE FROM product WHERE vendor_id = %s AND product_url NOT IN ({format_strings});"
