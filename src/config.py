import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_SECRET = os.getenv("MYSQL_SECRET", "password")
MYSQL_PORT = os.getenv("MYSQL_PORT", "33066")
MYSQL_DB = os.getenv("MYSQL_DB", "dev")