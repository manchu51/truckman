import functools
from sqlalchemy import func
from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.utils import redirect
from truck import db
from truck.models import Cost
from truck.forms import CostForm, CostPeriodForm, CostClassPeriodForm, DeleteForm
from truck.views.auth_views import login_required

from flask_wtf.csrf import CSRFProtect
import logging

COST_CLASS_CHOICES = {
    'D': '경유',
    'G': '휘발유',
    'E': '전기충전',
    'T': '차량관리',
    'N': '생필품',
    'M': '식대',
    'F': '면세품목',
    'O': '기타'
}

PAYMENT_CHOICES = {
    'E': '전자세금계산서',
    'P': '종이세금계산서',
    'S': '간이세금계산서',
    'C': '카드',
    'R': '간이영수증',
    'M': '현금영수증',
    'O': '기타'
}

bp = Blueprint('cost', __name__, url_prefix='/cost')


@bp.route('/cost/create/', methods=['GET', 'POST'])
@login_required
def create():
    costs = []  # Initialize costs to an empty list or appropriate default value

    form = CostForm()
    now_today = datetime.today().date()  # Today’s date
    today = datetime.today()
    user_id = session.get('user_id')    # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        # 세션에서 올바른 사용자 ID가 있는지 확인
        # flash(f'Logged in user ID: {session.get("user_id")}')
        # flash(f'Logged in as: {g.user.username}')

        cost = Cost(cost_date=form.cost_date.data, cost_company=form.cost_company.data,
                cost_class=form.cost_class.data, statement=form.statement.data,
                        payment=form.payment.data, bank_card=form.bank_card.data,
                            cost_amount=form.cost_amount.data, memo=form.memo.data,
                                    user_id=user_id)

        db.session.add(cost)
        db.session.commit()
        flash(f'Cost table for {form.cost_company.data} added successfully.')

        # Retrieve costs only for the logged-in user
        costs = Cost.query.filter(
            Cost.cost_date == now_today, Cost.user_id == user_id
        ).all()

    return render_template('cost/cost_form.html', form=form,
                today=today, costs=costs, cost_class_choices=COST_CLASS_CHOICES,
                        payment_choices=PAYMENT_CHOICES, enumerate=enumerate)


@bp.route('/cost_period', methods=['GET', 'POST'])
@login_required
def cost_period():
    form = CostPeriodForm()
    costs = []
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():

        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                costs = Cost.query.filter(
                    Cost.cost_date.between(start_date, end_date), Cost.user_id == user_id
                ).order_by(Cost.cost_date.desc()).all()

                if not costs:
                    flash('No records found for the selected period.', 'warning')

                return render_template('cost/cost_period_results.html',
                        costs=costs, cost_class_choices=COST_CLASS_CHOICES,
                                    payment_choices=PAYMENT_CHOICES, enumerate=enumerate)

            except ValueError:
                flash('Invalid date format.', 'danger')
        else:
            flash('Please enter both dates.', 'warning')

    return render_template('cost/cost_period.html', form=form)


@bp.route('/cost_modify/<int:id>', methods=['GET', 'POST'])
@login_required
def cost_modify(id):
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    # 수정하려는 비용 항목 가져오기
    cost = Cost.query.get_or_404(id)

    # 사용자가 해당 비용 항목의 소유자인지 확인
    if cost.user_id != user_id:
        flash("You do not have permission to modify this cost entry.", 'danger')
        return redirect(url_for('cost.cost_period'))

    # 비용 수정 폼 생성 및 기존 값으로 초기화
    form = CostForm(obj=cost)

    if form.validate_on_submit():
        try:
            # 수정된 데이터 폼으로부터 가져와서 객체 필드에 일괄 적용
            form.populate_obj(cost)
            cost.modify_date = datetime.now()  # 수정한 날짜 저장

            db.session.commit()
            flash('경비 정보가 수정 되었습니다.', 'success')
            return redirect(url_for('cost.cost_period'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the cost entry: {str(e)}', 'danger')

    return render_template('cost/cost_modify.html', form=form, cost=cost)


@bp.route('/cost_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def cost_delete(id):
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    # 삭제할 비용 항목 가져오기
    cost = Cost.query.get_or_404(id)

    # 사용자가 해당 비용 항목의 소유자인지 확인
    if cost.user_id != user_id:
        flash("You do not have permission to delete this cost entry.", 'danger')
        return redirect(url_for('cost.cost_period'))

    # 삭제 확인 폼
    form = DeleteForm()

    # POST 요청 및 폼 유효성 검사
    if form.validate_on_submit():
        db.session.delete(cost)
        db.session.commit()
        flash('경비 정보가 삭제되었습니다.', 'success')
        return redirect(url_for('cost.cost_period'))  # 원하는 페이지로 리다이렉트

    # 삭제 확인 페이지 렌더링
    return render_template('cost/cost_delete.html', form=form, cost=cost)


@bp.route('/cost_class_period', methods=['GET', 'POST'])
@login_required
def cost_class_period():
    form = CostClassPeriodForm()
    costs = None
    total_cost_amount = 0
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        # Use form data directly instead of request.form
        cost_class = form.cost_class.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Check that start_date and end_date are provided
        if start_date and end_date:
            try:
                # Convert start_date and end_date to datetime objects (optional if form already validates it)
                start_date = datetime.combine(start_date, datetime.min.time())
                end_date = datetime.combine(end_date, datetime.max.time())

                # Fetch cost records and total amount in a single query
                costs = Cost.query.filter(
                    Cost.cost_class == cost_class,
                    Cost.cost_date.between(start_date, end_date),
                    Cost.user_id == user_id
                ).order_by(Cost.cost_date.desc()).all()

                # Calculate total cost amount
                total_cost_amount = db.session.query(
                    func.sum(Cost.cost_amount)
                ).filter(
                    Cost.cost_class == cost_class,
                    Cost.cost_date.between(start_date, end_date),
                    Cost.user_id == user_id
                ).scalar() or 0  # Default to 0 if no results

                if not costs:
                    flash('검색 결과가 없습니다.', 'warning')

                return render_template('cost/cost_class_results.html',
                    costs=costs, total_cost_amount=total_cost_amount, cost_class=cost_class,
                        cost_class_choices=COST_CLASS_CHOICES,
                            payment_choices=PAYMENT_CHOICES, enumerate=enumerate)

            except ValueError:
                flash('Invalid date format.', 'danger')
        else:
            flash('Please enter both dates.', 'warning')

    return render_template('cost/cost_class_period.html', form=form)
