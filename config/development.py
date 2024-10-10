import os
from config.default import *

# __init__.py 에서 로드됨 중복 제거
#from dotenv import load_dotenv
#load_dotenv()  # Load environment variables from .env file

db = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SECRET_KEY = "dev"
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Ensure that the SECRET_KEY is a valid string
if not isinstance(SECRET_KEY, str):
    raise TypeError("SECRET_KEY must be a string")

# development.py
MAIL_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
MAIL_PORT = 587  # Port used for TLS
MAIL_USE_TLS = True  # Enable TLS
MAIL_USE_SSL = False  # Disable SSL (since we're using TLS)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Your Gmail address
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # App password or Gmail password
MAIL_DEFAULT_SENDER = ('김영실', os.getenv('MAIL_USERNAME'))  # Sender's name and email

