from collections import defaultdict
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, session, g, flash
from .. import db
from truck.models import Transport, Cost, Company
from sqlalchemy import func  # SQLAlchemy의 func 임포트
from truck.forms import BalancePeriodForm, TaxPeriodForm, PaperPeriodForm, ElectPeriodForm
from truck.views.auth_views import login_required
from sqlalchemy import or_
from sqlalchemy.orm import aliased


from flask import Blueprint, render_template

bp = Blueprint('guide', __name__, url_prefix='/guide')


@bp.route('/company_introduce')
def company_introduce():
    return render_template('guide/company_introduce.html')


@bp.route('/terms_use')
def terms_use():
    return render_template('guide/terms_use.html')


@bp.route('guide')
def show_guide():
    return render_template('guide/guide.html')


@bp.route('/conditions')
def terms_condition():
    return render_template('guide/terms_condition.html')


@bp.route('/customer')
def customer_service():
    return render_template('guide/customer_service.html')


@bp.route('/terms_privite')
def terms_privite():
    return render_template('guide/terms_privite.html')


@bp.route('/faq')
def faq():
    return render_template('guide/faq.html')


@bp.route('/survey')
def survey():
    return render_template('guide/survey.html')


@bp.route('/sticker')
def sticker():
    return render_template('guide/sticker.html')


