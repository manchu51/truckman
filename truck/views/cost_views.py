from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
from flask_wtf.csrf import CSRFProtect
from .. import db
from truck.models import Cost
from sqlalchemy import func  # SQLAlchemy의 func 임포트

from truck.forms import CostForm, CostPeriodForm, CostClassPeriodForm
from truck.forms import DeleteForm
from truck.views.auth_views import login_required


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


@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = CostForm()
    now_today = datetime.today().date()  # 오늘 날짜를 가져옵니다.
    today = datetime.today()
    if request.method == 'POST' and form.validate_on_submit():
        cost = Cost(cost_date=form.cost_date.data, cost_company=form.cost_company.data,
                cost_class=form.cost_class.data, statement=form.statement.data, payment=form.payment.data,
                    bank_card=form.bank_card.data, cost_amount=form.cost_amount.data, memo=form.memo.data)

        db.session.add(cost)
        db.session.commit()
        flash(f'Cost table {form.cost_company.data} added successfully.')
        # flash('Cost Table added successfully.')
        return redirect(url_for('cost.create', today=today))

    # 오늘 날짜로 입력된 모든 transport 데이터를 가져옵니다.
    costs = Cost.query.filter(
        Cost.cost_date == now_today
    ).all()

    return render_template('cost/cost_form.html', form=form, today=today,
                costs=costs, cost_class_choices=COST_CLASS_CHOICES, payment_choices=PAYMENT_CHOICES,
                           enumerate=enumerate)


@bp.route('/cost_period', methods=['GET', 'POST'])
@login_required
def cost_period():
    form = CostPeriodForm()  # 들여쓰기를 수정합니다.
    #costs = None
    costs = []
    if request.method == 'POST' and form.validate_on_submit():
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                # cost 테이블에서 지정된 기간 동안의 데이터를 조회하고 역순으로 정렬
                costs = Cost.query.filter(
                    Cost.cost_date >= start_date,
                    Cost.cost_date <= end_date
                ).order_by(Cost.cost_date.desc()).all()

                if not costs:
                    flash('검색 결과가 없습니다.', 'warning')
                return render_template('cost/cost_period_results.html',
                        costs=costs, cost_class_choices=COST_CLASS_CHOICES,
                                    payment_choices=PAYMENT_CHOICES, enumerate=enumerate)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('cost/cost_period.html', form=form)


@bp.route('/cost_modify/<int:id>', methods=['GET', 'POST'])
@login_required
def cost_modify(id):
    cost = Cost.query.get_or_404(id)
    if request.method == 'POST':
        modify_date = datetime.now()

        cost.cost_date = request.form['cost_date']
        cost.modify_date = modify_date
        cost.cost_company = request.form['cost_company']
        cost.cost_class = request.form['cost_class']
        cost.statement = request.form['statement']
        cost.payment = request.form['payment']
        cost.bank_card = request.form['bank_card']
        cost.cost_amount = request.form['cost_amount']
        cost.memo = request.form['memo']

        db.session.commit()

        flash('Cost table modified successfully.')
        return redirect(url_for('cost.cost_period'))
    return render_template('cost/cost_modify.html', cost=cost)


@bp.route('/cost_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def cost_delete(id):
    cost = Cost.query.get_or_404(id)
    form = DeleteForm()
    if request.method == 'POST':
        db.session.delete(cost)
        db.session.commit()
        flash('경비가 삭제되었습니다.', 'success')
        return redirect(url_for('cost.cost_period'))
    return render_template('cost/cost_delete.html', form=form, cost=cost)


@bp.route('/cost_class_period', methods=['GET', 'POST'])
@login_required
def cost_class_period():
    form = CostClassPeriodForm()  # 들여쓰기를 수정합니다.
    costs = None
    if request.method == 'POST' and form.validate_on_submit():
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                # cost 테이블에서 지정된 기간 동안의 데이터를 조회하고 역순으로 정렬
                costs = Cost.query.filter(
                    Cost.cost_date >= start_date,
                    Cost.cost_date <= end_date
                ).order_by(Cost.cost_date.desc()).all()

                # 비용 합계를 계산하는 쿼리
                total_cost_amount = Cost.query.with_entities(
                    func.sum(Cost.cost_amount)).filter(
                        Cost.cost_date >= start_date,
                        Cost.cost_date <= end_date
                ).scalar()

                # 만약 특정 cost_class를 필터링하려는 경우

                if not costs:
                    flash('검색 결과가 없습니다.', 'warning')
                return render_template('cost/cost_class_results.html',
                        costs=costs, total_cost_amount=total_cost_amount,
                            cost_class_choices=COST_CLASS_CHOICES,
                                payment_choices=PAYMENT_CHOICES, enumerate=enumerate)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('cost/cost_class_period.html', form=form)


"""
 #cost_class = [cost.cost_class for cost in costs] if costs else None
"""