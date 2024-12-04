import os
from dotenv import load_dotenv
load_dotenv()

class DatabaseConfig:
    HOST = os.getenv('DB_HOST', 'localhost')
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = os.getenv('DB_NAME', 'manisa2')
    PORT = int(os.getenv('DB_PORT', 3306))

    @classmethod
    def get_config(self):
        return {
            'host': self.HOST,
            'user': self.USER,
            'password': self.PASSWORD,
            'database': self.DATABASE,
            'port': self.PORT
        }