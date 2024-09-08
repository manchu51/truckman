import os
from config.default import *

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://manchu51:espoire51@localhost/truckman'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '3206e2397effc47e81eb208b4a84691f264e4e807bfb81984ad9b74e44fa7be8'

