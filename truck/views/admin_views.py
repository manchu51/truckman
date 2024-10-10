from functools import wraps  # Import wraps

from datetime import datetime, timedelta, date
from sqlalchemy import func
from flask import Blueprint, url_for, render_template, flash, request, session, g

from werkzeug.utils import redirect
from truck import db
from truck.models import User, Cost, Company      # Import the User model
from truck.views.auth_views import login_required

from flask_wtf.csrf import CSRFProtect
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# Ensure that only admins can access these routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            return redirect(url_for('auth.login'))  # Redirect non-admin users
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # 세션이나 current_user에서 사용자 정보를 가져옴
    user_id = session.get('user_id')

    # user_id가 세션에 없다면 로그인 페이지로 리디렉션
    if not user_id:
        return redirect(url_for('auth.login'))

    # User 모델에서 user_id로 사용자 정보 조회
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for('auth.login'))

    total_users = User.query.count()
    total_costs = Cost.query.count()
    new_register_today = User.query.filter(User.register_date == date.today()).count()
    total_revenue = Cost.query.with_entities(func.sum(Cost.cost_amount)).scalar() or 0

    return render_template(
        'admin/dashboard.html',
        user=user,
        username=session.get('username'),
        total_users=total_users,
        total_costs=total_costs,
        new_register_today=new_register_today,
        total_revenue=total_revenue
    )


"""
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)  # Fetch user from the database
        if user:
            return render_template('admin/dashboard.html', user=user)
        else:
            return "User not found", 404  # Add a check for missing user
    else:
        return redirect(url_for('auth.login'))
"""


@admin_bp.route('/admin/manage_users/', methods=['GET'])
@login_required
@admin_required
def manage_users():
    # Logic for displaying and managing users

    # 오늘 날짜와 15일 이전 날짜 계산
    today = datetime.today()
    fifteen_days_ago = today - timedelta(days=315)

    # URL 매개변수로부터 현재 페이지 가져오기, 기본값은 1
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 한 페이지당 표시할 데이터 개수

    # user 테이블에서 15일 이내에 가입한 회원 정보 조회
    users = User.query.filter(User.register_date >= fifteen_days_ago).paginate(page=page, per_page=per_page)
    #users = User.query.filter(User.register_date >= fifteen_days_ago).paginate(page=page, per_page=per_page)
    # 총 회원 수 계산
    total_users = User.query.count()

    return render_template('admin/manage_users.html', users=users, today=today,
                           total_users=total_users, page=page, per_page=per_page)


@admin_bp.route('/admin/manage_costs/', methods=['GET'])
@login_required
@admin_required
def manage_costs():
    costs = Cost.query.all()  # Admin can see all costs
    return render_template('admin/cost_form.html', costs=costs)

