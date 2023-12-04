from data.coffee_vendors_data import coffee_vendors_data


def append_vendor_data_to_seed_sql(vendor_data):
    seed_vendor_sql = "\n\n-- Seed the vendor table\n"
    values = []

    for vendor in vendor_data:
        vendor_name_escaped = vendor["vendor"].replace("'", "''")
        currency_escaped = vendor["currency"].replace("'", "''")
        vendor_location_escaped = vendor["vendor_location"].replace("'", "''")
        value = f"('{vendor_name_escaped}', (SELECT id FROM currency_code WHERE code = '{currency_escaped}'), (SELECT id FROM country WHERE name = '{vendor_location_escaped}'))"
        values.append(value)

    # Combine values and add conflict resolution
    if values:
        seed_vendor_sql += "INSERT INTO vendor (name, currency_code_id, country_id) VALUES\n"
        seed_vendor_sql += ",\n".join(values)
        seed_vendor_sql += "\nON CONFLICT (name) DO NOTHING;\n"

    # Write to seed.sql file
    with open('supabase/seed.sql', 'a') as file:
        file.write(seed_vendor_sql)


# Call the function with the path to the seed.sql file
append_vendor_data_to_seed_sql(coffee_vendors_data)
