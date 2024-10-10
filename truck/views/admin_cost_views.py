import functools
from sqlalchemy import func
from datetime import datetime, date
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.utils import redirect
from truck import db
from truck.models import Cost
from truck.forms import CostForm, CostPeriodForm, CostClassPeriodForm, DeleteForm
from truck.views.admin_views import admin_required
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

admin_cost_bp = Blueprint('admin_cost', __name__, url_prefix='/admin/cost')


@admin_cost_bp.route('/create/', methods=['GET', 'POST'])
@admin_required
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

        print(f"Costs: {costs}")

    return render_template('admin/cost/cost_form.html', form=form,
                today=today, costs=costs, cost_class_choices=COST_CLASS_CHOICES,
                           payment_choices=PAYMENT_CHOICES, enumerate=enumerate)


@admin_cost_bp.route('/cost_period/', methods=['GET', 'POST'])
@admin_required
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

                return render_template('admin/cost/cost_period_results.html',
                        costs=costs, cost_class_choices=COST_CLASS_CHOICES,
                                    payment_choices=PAYMENT_CHOICES, enumerate=enumerate)

            except ValueError:
                flash('Invalid date format.', 'danger')
        else:
            flash('Please enter both dates.', 'warning')

    return render_template('admin/cost/cost_period.html', form=form)


@admin_cost_bp.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_cost_modify(id):
    cost = Cost.query.get_or_404(id)  # 비용 항목 가져오기

    form = CostForm(obj=cost)  # 비용 항목 데이터로 폼 초기화

    if form.validate_on_submit():
        try:
            # 수정된 데이터 폼으로부터 가져와서 객체 필드에 일괄 적용
            form.populate_obj(cost)
            cost.modify_date = datetime.now()  # 수정 날짜 업데이트

            db.session.commit()
            flash('Cost entry modified successfully.', 'success')

            return redirect(url_for('admin_cost.cost_period'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the cost entry: {str(e)}', 'danger')

    return render_template('admin/cost/cost_modify_origin.html', form=form, cost=cost)


@admin_cost_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_cost_delete(id):
    cost = Cost.query.get_or_404(id)    # 삭제할 비용 항목 가져오기

    form = DeleteForm()                 # 삭제 확인 폼

    if form.validate_on_submit():
        try:
            db.session.delete(cost)
            db.session.commit()
            flash('Cost entry deleted successfully.', 'success')
            return redirect(url_for('admin_cost.cost_period'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while deleting the cost entry: {str(e)}', 'danger')

    return render_template('admin/cost/cost_delete.html', form=form, cost=cost)


@admin_cost_bp.route('/cost_class_period/', methods=['GET', 'POST'])
@admin_required
def cost_class_period():
    form = CostClassPeriodForm()
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

                total_cost_amount = Cost.query.with_entities(
                    func.sum(Cost.cost_amount)).filter(
                    Cost.cost_date >= start_date,
                    Cost.cost_date <= end_date).scalar()

                if not costs:
                    flash('No results found.', 'warning')

                return render_template('admin/cost/cost_class_results.html',
                        costs=costs, total_cost_amount=total_cost_amount,
                            cost_class_choices=COST_CLASS_CHOICES, payment_choices=PAYMENT_CHOICES,
                                enumerate=enumerate)

            except ValueError:
                flash('Invalid date format.', 'danger')
        else:
            flash('Please enter both dates.', 'warning')

    return render_template('admin/cost/cost_class_period.html', form=form)


"""
@admin_cost_bp.route('/manage', methods=['GET'])
@admin_required
def manage_costs():
    user_id = session.get('user_id')    # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    costs = Cost.query.filter(          # 모든 비용 항목 조회
        Cost.user_id == user_id
        ).order_by(Cost.cost_date.desc()   # Cost.cost_date.between(start_date, end_date
    ).all()

    return render_template('admin/cost/admin_manage_costs.html',
            costs=costs, cost_class_choices=COST_CLASS_CHOICES, payment_choices=PAYMENT_CHOICES)
"""

