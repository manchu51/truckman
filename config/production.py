import os
#from flask import Flask
#from flask_mail import Mail
from config.default import *

# MySQL 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://truckman:espoire5104@truckman.mysql.pythonanywhere-services.com:3306/truckman$truckman?charset=utf8mb4'
)

# SQLAlchemy 수정 사항 추적 비활성화
SQLALCHEMY_TRACK_MODIFICATIONS = False

# .env 파일에서 SECRET_KEY 가져오기
SECRET_KEY = os.getenv('SECRET_KEY')

# SECRET_KEY가 설정되지 않았을 경우 오류 발생
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application. Did you forget to set it in the .env file?")

# development.py
MAIL_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
MAIL_PORT = 587  # Port used for TLS
MAIL_USE_TLS = True  # Enable TLS
MAIL_USE_SSL = False  # Disable SSL (since we're using TLS)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Your Gmail address
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # App password or Gmail password
MAIL_DEFAULT_SENDER = ('김영실', os.getenv('MAIL_USERNAME'))  # Sender's name and email

#mail = Mail(app)


