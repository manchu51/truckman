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


@bp.route('guide')
def show_guide():
    return render_template('guide/guide.html')
