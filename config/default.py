import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class DefaultConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 86400  # 24시간 (초 단위)
