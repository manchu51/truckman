import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variables directly to build the SQLAlchemy URL
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8"
)

# Disable modification tracking for SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Use the SECRET_KEY from .env
SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')  # Fallback to a default key if not set
