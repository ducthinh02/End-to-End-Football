import psycopg2
import os
from dotenv import load_dotenv 
from core.Exceptions import ConfigurationError

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

if not POSTGRES_USER:
    raise ConfigurationError("POSTGRES_USER not found in .env")

if not POSTGRES_PASSWORD:
    raise ConfigurationError("POSTGRES_PASSWORD not found in .env")

if not POSTGRES_DB:
    raise ConfigurationError("POSTGRES_DB not found in .env")

if not POSTGRES_HOST:
    raise ConfigurationError("POSTGRES_HOST not found in .env")

if not POSTGRES_PORT:
    raise ConfigurationError("POSTGRES_PORT not found in .env")


class DatabaseConnection:
    def __init__(self):
        
        try:
            self.conn = psycopg2.connect(
                        database=POSTGRES_DB,
                        user=POSTGRES_USER,
                        host=POSTGRES_HOST,
                        password=POSTGRES_PASSWORD,
                        port=int(POSTGRES_PORT))
        except psycopg2.Error as e:

            raise ConfigurationError(
                f"Cannot connect PostgreSQL: {e}"
            )
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None