import MySQLdb
from db.db_connection import DBConnection
from db.queries import get_id_by_process_category_name_query, seed_process_category_query
from enums.process_category import ProcessCategory
from config.logger_config import logger


try:
    db_connection = DBConnection()
    connection = db_connection.get_connection()
    cursor = connection.cursor()

    # Iterate through the enum and insert each process category
    for category in ProcessCategory:
        # Check if the category already exists to avoid duplicates
        cursor.execute(
            get_id_by_process_category_name_query, (category.value,))
        if cursor.fetchone() is None:  # Only insert if the category doesn't exist
            cursor.execute(seed_process_category_query, (category.value,))
            logger.info(
                f"Inserted {category.value} into ProcessCategory table.")

    # Commit the changes
    connection.commit()

except MySQLdb.Error as e:
    logger.error(f"Database error: {e}")

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        logger.info("Database connection closed.")
