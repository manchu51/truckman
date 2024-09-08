import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

csrf = CSRFProtect()


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
    app.config.from_envvar('APP_CONFIG_FILE')   #app.config.from_object(config)

    # ORM 초기화   # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize CSRF protection
    csrf.init_app(app)

    # 모델 가져오기
    from . import models

    # Register blueprints
    from .views import (main_views, question_views, answer_views,
                        auth_views, transport_views, cost_views, company_views,
                        balance_views, guide_views)

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(transport_views.bp)
    app.register_blueprint(cost_views.bp)
    app.register_blueprint(company_views.bp)
    app.register_blueprint(balance_views.bp)
    app.register_blueprint(guide_views.bp)


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

    return app

# 애플리케이션 객체 생성
app = create_app()