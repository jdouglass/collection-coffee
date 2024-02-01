import psycopg2
from config.config_loader import get_env_variable

class DBConnection:
    def __init__(self):
        self.host = get_env_variable('DB_HOST')
        self.port = get_env_variable('DB_PORT')
        self.user = get_env_variable('DB_USERNAME')
        self.password = get_env_variable('DB_PASSWORD')
        self.db_name = get_env_variable('DB_NAME')

    def get_connection(self):
        connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.db_name,
        )
        return connection
