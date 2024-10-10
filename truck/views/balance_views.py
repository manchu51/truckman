from collections import defaultdict
from datetime import datetime
from flask import Blueprint, render_template, flash, request, redirect, url_for, session, g
from werkzeug.utils import redirect
from .. import db
from truck.models import Transport, Cost, Company
from sqlalchemy import func  # SQLAlchemy의 func 임포트
from truck.forms import BalancePeriodForm, TaxPeriodForm, PaperPeriodForm, ElectPeriodForm
from truck.views.auth_views import login_required
from sqlalchemy import or_
from sqlalchemy.orm import aliased

# Example choices definition
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
    'C': '카드발급',
    'R': '간이영수증',
    'M': '현금영수증',
    'O': '기타'
}

bp = Blueprint('balance', __name__,  url_prefix='/balance')


@bp.route('/balance_period/', methods=['GET', 'POST'])
@login_required
def balance_period():
    form = BalancePeriodForm()
    transports = []
    costs = []
    today = datetime.now()  # Get the current date and time

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Assuming you have defined models Transport and Cost and a method to get the relevant data
        transports = Transport.query.filter(
            Transport.trans_date >= start_date, Transport.trans_date <= end_date,
                Transport.trans_type == 'N', Transport.user_id == user_id
        ).all()

        costs = Cost.query.filter(
            Cost.cost_date >= start_date, Cost.cost_date <= end_date, Cost.user_id == user_id
        ).all()

        # Group data by date
        grouped_data = defaultdict(lambda: {'transports': [], 'costs': []})
        for transport in transports:
            grouped_data[transport.trans_date]['transports'].append(transport)
        for cost in costs:
            grouped_data[cost.cost_date]['costs'].append(cost)

        # Calculate total number of items
        total_items = len(transports) + len(costs)

        # No need to convert dates since they are already datetime.date objects
        sorted_dates = sorted(grouped_data.keys())

        return render_template('balance/balance_period_results.html',
                form=form, cost_class_choices=Cost.COST_CLASS_CHOICES, today=today,
                    payment_choices=Cost.PAYMENT_CHOICES, transports=transports,
                            costs=costs, grouped_data=grouped_data, sorted_dates=sorted_dates,
                               max=max, Cost=Cost, total_items=total_items, enumerate=enumerate)

    return render_template('balance/balance_period.html', form=form)


@bp.route('/tax_period/', methods=['GET', 'POST'])
@login_required
def tax_period():
    form = TaxPeriodForm()
    results = []

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Cost 테이블을 LEFT JOIN으로 그룹화, user_id로 필터링
        results = (
            db.session.query(
                func.any_value(Company.business_no).label('business_no'),  # ANY_VALUE 사용
                Cost.cost_company,
                func.count(Cost.id).label('company_count'),
                func.sum(Cost.cost_amount).label('total_amount')
            )
            .outerjoin(Cost, Cost.cost_company == Company.firm)  # LEFT OUTER JOIN
            .filter(
                Cost.user_id == user_id,  # Cost 테이블에서 user_id 필터 추가
                Company.user_id == user_id,  # Company 테이블에서 user_id 필터 추가
                Cost.cost_date.between(start_date, end_date),
                Company.company_class == 'P'
            )
            .group_by(Cost.cost_company)
            .all()
        )

        # 총 금액 계산
        total_amount = sum([row.total_amount for row in results])
        company_count = sum([row.company_count for row in results])

        if not results:
            flash('검색 결과가 없습니다.', 'warning')

        return render_template('balance/cost_tax.html', form=form,
                        results=results, total_amount=total_amount, company_count=company_count,
                               enumerate=enumerate)

    return render_template('balance/tax_period.html', form=form)



@bp.route('/paper_period/', methods=['GET', 'POST'])
@login_required
def paper_period():
    form = PaperPeriodForm()
    results = []
    total_amount = 0  # 초기값을 0으로 설정

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # 첫 번째 쿼리: 특정 조건에 맞는 Transport 데이터를 가져오기
        transports = Transport.query.filter(
                Transport.payment == 'P',  Transport.user_id == user_id,
                        Company.user_id == user_id,
            or_(
                Transport.terms.in_(['TP', 'TF']),
                Transport.terms.in_(['CP', 'CF']),
                Transport.terms.in_(['DP', 'DF'])
            )
        ).all()

        company_data = {}  # 중복을 방지하기 위한 딕셔너리

        for transport in transports:
            company = None
            if transport.terms in ['TP', 'TF']:
                company = Company.query.filter_by(
                    firm=transport.trans_company).first()
            elif transport.terms in ['CP', 'CF']:
                company = Company.query.filter_by(firm=transport.consignor).first()
            elif transport.terms in ['DP', 'DF']:
                company = Company.query.filter_by(firm=transport.consignee).first()

            if company:
                key = (company.business_no, company.firm)
                if key not in company_data:
                    company_data[key] = {
                        'business_no': company.business_no,
                        'name': company.firm,
                        'count': 0,
                        'total_amount': 0,
                        'total_tax': 0
                    }

                # 회사별로 집계 데이터 추가
                company_data[key]['count'] += 1
                company_data[key]['total_amount'] += transport.trans_amount
                company_data[key]['total_tax'] += transport.trans_amount / 10

            # company_data를 results로 변환
            results = list(company_data.values())
            total_amount = sum(item['total_amount'] for item in results)

        if not results:
            flash('검색 결과가 없습니다.', 'warning')

        return render_template('balance/paper_tax.html', form=form,
                               results=results, total_amount=total_amount,
                               enumerate=enumerate)

    return render_template('balance/paper_period.html', form=form)


@bp.route('/elect_period/', methods=['GET', 'POST'])
@login_required
def elect_period():
    form = ElectPeriodForm()
    results = []
    total_amount = 0  # 초기값을 0으로 설정

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

        # 첫 번째 쿼리: 특정 조건에 맞는 Transport 데이터를 가져오기
        transports = Transport.query.filter(
            Transport.payment == 'E',   Transport.user_id == user_id,
                        Company.user_id == user_id,
            or_(
                Transport.terms.in_(['TP', 'TF']),
                Transport.terms.in_(['CP', 'CF']),
                Transport.terms.in_(['DP', 'DF'])
            )
        ).all()

        company_data = {}  # 중복을 방지하기 위한 딕셔너리

        for transport in transports:
            company = None
            if transport.terms in ['TP', 'TF']:
                company = Company.query.filter_by(firm=transport.trans_company).first()
            elif transport.terms in ['CP', 'CF']:
                company = Company.query.filter_by(firm=transport.consignor).first()
            elif transport.terms in ['DP', 'DF']:
                company = Company.query.filter_by(firm=transport.consignee).first()

            if company:
                key = (company.business_no, company.firm)
                if key not in company_data:
                    company_data[key] = {
                        'business_no': company.business_no,
                        'name': company.firm,
                        'count': 0,
                        'total_amount': 0,
                        'total_tax': 0
                    }

                # 회사별로 집계 데이터 추가
                company_data[key]['count'] += 1
                company_data[key]['total_amount'] += transport.trans_amount
                company_data[key]['total_tax'] += transport.trans_amount / 10

            # company_data를 results로 변환
            results = list(company_data.values())
            total_amount = sum(item['total_amount'] for item in results)

        if not results:
            flash('검색 결과가 없습니다.', 'warning')

        return render_template('balance/elect_tax.html', form=form,
                               results=results, total_amount=total_amount,
                               enumerate=enumerate)

    return render_template('balance/elect_period.html', form=form)

