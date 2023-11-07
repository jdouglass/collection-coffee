from dotenv import load_dotenv
from db.db_connection import DBConnection
from data.coffee_vendors_data import coffee_vendors_data
from config.logger_config import logger
from db.queries import seed_vendor_query, get_id_by_country_name_query, get_id_by_currency_code_query


load_dotenv()


db_connection = DBConnection()
connection = db_connection.get_connection()
cursor = connection.cursor()


def insert_vendor_data(connection, vendor_name, country_id, currency_id):
    with connection.cursor() as cursor:
        cursor.execute(seed_vendor_query,
                       (vendor_name, country_id, currency_id))


def get_country_id(connection, country_name):
    with connection.cursor() as cursor:
        cursor.execute(
            get_id_by_country_name_query, (country_name,))
        result = cursor.fetchone()
        return result[0] if result else None


def get_currency_id(connection, currency_code):
    with connection.cursor() as cursor:
        cursor.execute(
            get_id_by_currency_code_query, (currency_code,))
        result = cursor.fetchone()
        return result[0] if result else None


def main():
    db_connection = DBConnection().get_connection()
    for vendor in coffee_vendors_data:
        vendor_name = vendor['vendor']
        country_name = vendor['vendor_location']
        currency_code = vendor['currency']

        country_id = get_country_id(db_connection, country_name)
        if country_id is None:
            raise ValueError(f"Country not found for {country_name}")

        currency_id = get_currency_id(db_connection, currency_code)
        if currency_id is None:
            raise ValueError(f"Currency not found for {currency_code}")

        insert_vendor_data(db_connection, vendor_name, country_id, currency_id)

    logger.info("Vendor data seeding completed.")


if __name__ == "__main__":
    main()
