import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_misaka import Misaka
from flask_mail import Mail
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()       # .env 파일을 로드

db = SQLAlchemy()   # 데이터베이스 객체 초기화
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()  # Mail 클래스로 mail 객체를 생성

def intcomma(value):
    """숫자에 쉼표를 추가하는 필터"""
    return f"{value:,}"
def page_not_found(e):
    return render_template('404.html'), 404
def create_app():
    app = Flask(__name__)

    # Flask 설정 파일 불러오기
    app.config.from_object('config.development')  # 예: development 설정 로드

    # 데이터베이스 초기화 및 마이그레이션 # ORM 초기화   # Initialize extensions
    db.init_app(app)            # SQLAlchemy 앱 초기화
    migrate.init_app(app, db)   # Migrate 객체에 Flask 앱과 db 전달

    csrf.init_app(app)   # Initialize CSRF protection
    mail.init_app(app)   # Flask-Mail 객체 초기화

    # 모델 가져오기
    from . import models

    # Register blueprints
    from .views import(
        main_views, question_views, answer_views, auth_views, transport_views,
        cost_views, company_views, balance_views, guide_views,
        admin_views)

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


