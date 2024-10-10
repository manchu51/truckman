import functools
from sqlalchemy import func
from datetime import datetime
from datetime import date
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.utils import redirect
from truck import db
from truck.models import Company, User
from truck.forms import CompanyForm, CompanyPeriodForm, DeleteForm, CompanyClassPeriodForm
from truck.views.auth_views import login_required

from flask_wtf.csrf import CSRFProtect
import logging

COMPANY_CLASS_CHOICES = {
    'R': '매출처',
    'P': '매입처'
}

bp = Blueprint('company', __name__, url_prefix='/company')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CompanyForm()
    now_today = datetime.today().date()  # 오늘 날짜를 가져옵니다.
    today = datetime.today()
    user_id = session['user_id']  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        company = Company(register_date=form.register_date.data, company_class=form.company_class.data,
            business_no=form.business_no.data, firm=form.firm.data, president=form.president.data,
                zip=form.zip.data, address=form.address.data, business_status=form.business_status.data,
                    business_item=form.business_item.data, email=form.email.data, cellphone=form.cellphone.data,
                        tel=form.tel.data, fax=form.fax.data,  note=form.note.data, user_id=user_id)

        db.session.add(company)
        db.session.commit()
        flash(f'Company table {form.firm.data} added successfully.')

        return redirect(url_for('company.create', today=today))

    # 오늘 날짜로 입력된 모든 transport 데이터를 가져옵니다.
    companies = Company.query.filter(
        Company.register_date == now_today, Company.user_id == user_id
    ).all()

    return render_template('company/company_form.html', form=form, today=today,
                companies=companies, enumerate=enumerate)


@bp.route('/company_period', methods=['GET', 'POST'])
@login_required
def company_period():
    form = CompanyPeriodForm()
    companies = []
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        start_date = request. form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                companies = Company.query.filter(
                    Company.register_date.between(start_date, end_date), Company.user_id == user_id
                ).order_by(Company.register_date.desc()).all()

                if not companies:
                    flash('검색 결과가 없습니다.', 'warning')
                return render_template('company/company_period_results.html',
                        companies=companies, company_class_choices=COMPANY_CLASS_CHOICES,
                                enumerate=enumerate)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('company/company_period.html', form=form)


@bp.route('/company/modify/<int:company_id>', methods=['GET', 'POST'])
@login_required
def modify_company(company_id):
    company = Company.query.get_or_404(company_id)
    form = CompanyForm(obj=company)  # Company 객체로부터 초기값 설정
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        form.populate_obj(company)  # 폼 데이터를 Company 객체에 반영
        db.session.commit()
        flash('업체 정보가 수정되었습니다.', 'success')
        return redirect(url_for('company.company_period'))

    return render_template('company/company_modify.html', form=form, company=company)


@bp.route('/delete_company/<int:company_id>', methods=['GET', 'POST'])
@login_required
def delete_company(company_id):
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    # 삭제할 비용 항목 가져오기
    company = Company.query.get_or_404(company_id)

    # 사용자가 해당 Company 항목의 소유자인지 확인
    if company.user_id != user_id:
        flash("You do not have permission to delete this cost entry.", 'danger')
        return redirect(url_for('company.company_period'))

    # 삭제 확인 폼
    form = DeleteForm()

    # POST 요청 및 폼 유효성 검사
    if request.method == 'POST':
        db.session.delete(company)
        db.session.commit()
        flash('Company entry deleted successfully.', 'success')
        return redirect(url_for('company.company_period'))

    # 삭제 확인 페이지 렌더링
    return render_template('company/company_delete.html', form=form, company=company)


@bp.route('/company_class_period', methods=['GET', 'POST'])
@login_required
def company_class_period():
    form = CompanyClassPeriodForm(company_class='P')  # 들여쓰기를 수정합니다.
    companies = None
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        company_class = form.company_class.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        if start_date and end_date:
            try:
                start_date = datetime.combine(start_date, datetime.min.time())
                end_date = datetime.combine(end_date, datetime.max.time())

                # company 테이블에서 지정된 기간 동안의 데이터를 조회하고 역순으로 정렬
                companies = Company.query.filter(
                    Company.company_class == company_class,
                    Company.register_date.between(start_date, end_date),
                    Company.user_id == user_id
                ).order_by(Company.register_date.desc()).all()

                # 만약 특정 cost_class를 필터링하려는 경우

                if not companies:
                    flash('검색 결과가 없습니다.', 'warning')
                return render_template('company/company_class_results.html',
                        companies=companies, company_class_choices=COMPANY_CLASS_CHOICES,
                                company_class=company_class, enumerate=enumerate)
            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('company/company_class_period.html', form=form)
