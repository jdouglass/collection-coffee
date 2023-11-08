import pycountry
import pycountry_convert as pc

# Function to get continent name from country code using pycountry_convert


def get_continent_name(country_code):
    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(
            continent_code)
        return continent_name
    except KeyError:
        return None


# Generate SQL seed query for the country table
seed_country_sql = "\n\n-- Seed the country table\n"
values = []

for country in pycountry.countries:
    continent_name = get_continent_name(country.alpha_2)
    if continent_name:
        # Escape single quotes in country and continent names
        country_name_escaped = country.name.replace("'", "''")
        continent_name_escaped = continent_name.replace("'", "''")
        value = f"('{country_name_escaped}', (SELECT id FROM continent WHERE name = '{continent_name_escaped}'))"
        values.append(value)

# Combine values and add conflict resolution
if values:
    seed_country_sql += "INSERT INTO country (name, continent_id) VALUES\n"
    seed_country_sql += ",\n".join(values)
    seed_country_sql += "\nON CONFLICT (name) DO NOTHING;\n"

# Write to seed.sql file
with open('supabase/seed.sql', 'a') as file:
    file.write(seed_country_sql)
