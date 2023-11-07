from dotenv import load_dotenv
from config.logger_config import logger
from db.queries import insert_continent_query, insert_country_query, insert_currency_code_query, insert_vendor_query
from db.db_connection import DBConnection
import pycountry_convert as pc
import pycountry
from enums.continent import Continent
import MySQLdb


load_dotenv()

db_connection = DBConnection()
connection = db_connection.get_connection()
cursor = connection.cursor()


def get_continent_name(country_alpha2):
    try:
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continent_name = pc.convert_continent_code_to_continent_name(
            continent_code)
        return continent_name
    except KeyError:
        # In case the continent cannot be determined
        return None


try:
    # Insert continents
    for continent_name in Continent:
        cursor.execute(insert_continent_query, (continent_name.value,))

    # Insert countries and their respective continents
    for country in pycountry.countries:
        continent_name = get_continent_name(country.alpha_2)
        if continent_name:  # Only insert if the continent could be determined
            cursor.execute(insert_country_query,
                           (country.name, continent_name))

    # Insert currency codes
    for currency in pycountry.currencies:
        cursor.execute(insert_currency_code_query, (currency.alpha_3,))

except MySQLdb.Error as e:
    logger.error(f"Error seeding the database: {e}")
finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()

logger.info("Seeding the world data has been completed.")
