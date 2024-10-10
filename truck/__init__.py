import os

from datetime import datetime
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_misaka import Misaka
from flask_mail import Mail, Message
from dotenv import load_dotenv

#from itsdangerous import URLSafeTimedSerializer as Serializer
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

csrf = CSRFProtect()

mail = Mail()  # Mail 클래스로 mail 객체를 생성

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 10000  # Token validity in seconds (1 hour)


def intcomma(value):
    """숫자에 쉼표를 추가하는 필터"""
    return f"{value:,}"


def page_not_found(e):
    return render_template('404.html'), 404


def create_app():
    app = Flask(__name__)

    # Flask 설정 불러오기
    app.config.from_object('config.development')  # 예: development 설정 로드

    #app.config.from_envvar('APP_CONFIG_FILE')

    # ORM 초기화   # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)  # Flask-Mail 객체 초기화

    # Initialize CSRF protection
    csrf.init_app(app)

    # 모델 가져오기
    from . import models

    # Register blueprints
    from .views import(
        main_views, question_views, answer_views, auth_views, transport_views,
        cost_views, company_views, balance_views, guide_views,
        admin_views, admin_cost_views, admin_company_views)

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(transport_views.bp)
    app.register_blueprint(cost_views.bp)
    app.register_blueprint(company_views.bp)
    app.register_blueprint(balance_views.bp)
    app.register_blueprint(guide_views.bp)
    app.register_blueprint(admin_views.admin_bp)
    app.register_blueprint(admin_cost_views.admin_cost_bp)
    app.register_blueprint(admin_company_views.admin_company_bp)

    # Ensure this is properly set up in your application factory or main file
    #app.register_blueprint(admin_cost, url_prefix='/admin')
    #app.register_blueprint(cost, url_prefix='/cost')

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # Jinja2 필터 정의 및 등록
    def default_if_none(value, default_value=''):
        return default_value if value is None else value

    app.jinja_env.filters['default_if_none'] = default_if_none

    # Flask 애플리케이션에 필터 등록
    app.jinja_env.filters['intcomma'] = intcomma

    # 오류 페이지  # Error handling
    app.register_error_handler(404, page_not_found)

    # markdown
    Misaka(app, extensions=['nl2br', 'fenced_code'])

    return app


