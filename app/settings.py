import os

from dotenv import load_dotenv

load_dotenv()

dbhost = os.getenv("DB_HOST")
dbusername = os.getenv("DB_USERNAME")
dbpassword = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
otp_exp_min = os.getenv("OTP_EXP_MIN", 10)
razor_key = os.getenv("razor_key")
razor_secret = os.getenv("razor_secret")
