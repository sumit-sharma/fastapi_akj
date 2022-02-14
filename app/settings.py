import os

from dotenv import load_dotenv

load_dotenv()

dbhost = os.getenv("DB_HOST")
dbusername = os.getenv("DB_USERNAME")
dbpassword = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
