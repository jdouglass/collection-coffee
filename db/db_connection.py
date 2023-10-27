import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    def __init__(self):
        self.host = os.environ.get('DB_HOST')
        self.user = os.environ.get('DB_USERNAME')
        self.password = os.environ.get('DB_PASSWORD')
        self.db_name = os.environ.get('DB_NAME')

    def get_connection(self):
        connection = MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.db_name,
            autocommit=True,
            ssl_mode="VERIFY_IDENTITY",
            ssl={
                "ca": "./config/cacert.pem"
            }
        )
        return connection
