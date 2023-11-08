import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    def __init__(self):
        self.host = os.environ.get('DB_HOST')
        self.port = os.environ.get('DB_PORT')
        self.user = os.environ.get('DB_USERNAME')
        self.password = os.environ.get('DB_PASSWORD')
        self.db_name = os.environ.get('DB_NAME')

    def get_connection(self):
        connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.db_name,
        )
        return connection
