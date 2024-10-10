import os
from config.default import *

# __init__.py 에서 로드됨 중복 제거
#from dotenv import load_dotenv
#load_dotenv()  # Load environment variables from .env file


# Use the PythonAnywhere MySQL database
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://truckman:espoire5104@truckman.mysql.pythonanywhere-services.com:3306/truckman$truckman'
)

# Disable modification tracking for SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Use the production SECRET_KEY from the .env file
SECRET_KEY = os.getenv('SECRET_KEY')

# Ensure that the SECRET_KEY is loaded correctly, otherwise raise an error
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application. Did you forget to set it in the .env file?")



