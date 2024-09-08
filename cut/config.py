import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

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
SECRET_KEY = "dev"



"""
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://manchu51:espoire51@localhost/truckman'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '3206e2397effc47e81eb208b4a84691f264e4e807bfb81984ad9b74e44fa7be8'

"""