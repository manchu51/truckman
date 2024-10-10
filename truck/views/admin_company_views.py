import functools
from sqlalchemy import func
from datetime import datetime, date
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.utils import redirect
from truck import db
from truck.models import Company, User
from truck.forms import CompanyForm, CompanyPeriodForm, DeleteForm, CompanyClassPeriodForm
from truck.views.admin_views import admin_required
from flask_wtf.csrf import CSRFProtect
import logging

COMPANY_CLASS_CHOICES = {
    'R': '매출처',
    'P': '매입처'
}

admin_company_bp = Blueprint('admin_company', __name__, url_prefix='/admin/company')


@admin_company_bp.route('/create/', methods=['GET', 'POST'])
@admin_required
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

        return redirect(url_for('admin_company.create', today=today))

    # 오늘 날짜로 입력된 모든 transport 데이터를 가져옵니다.
    companies = Company.query.filter(
        Company.register_date == now_today, Company.user_id == user_id
    ).all()

    return render_template('admin/company/company_form.html', form=form, today=today,
                companies=companies, enumerate=enumerate)


@admin_company_bp.route('/company_period/', methods=['GET', 'POST'])
@admin_required
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
                return render_template('admin/company/company_period_results.html',
                        companies=companies, company_class_choices=COMPANY_CLASS_CHOICES,
                                enumerate=enumerate)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('admin/company/company_period.html', form=form)


@admin_company_bp.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_company_modify(id):
    company = Company.query.get_or_404(id)

    form = CompanyForm(obj=company)  # Company 객체로부터 초기값 설정

    if form.validate_on_submit():
        try:
            # 수정된 데이터 폼으로부터 가져와서 객체 필드에 일괄 적용. 폼 데이터를 Company 객체에 반영
            form.populate_obj(company)
            company.modify_date = datetime.now()  # 수정 날짜 업데이트

            db.session.commit()
            flash('Cost entry modified successfully.', 'success')

            return redirect(url_for('admin_company.company_period'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the cost entry: {str(e)}', 'danger')

    return render_template('admin/company/company_modify.html', form=form, company=company)


@admin_company_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_company_delete(id):
    company = Company.query.get_or_404(id)       # 삭제할 회사 항목 가져오기

    form = DeleteForm()                 # 삭제 확인 폼

    if form.validate_on_submit():       # POST 요청 및 폼 유효성 검사
        try:
            db.session.delete(company)
            db.session.commit()
            flash('Company entry deleted successfully.', 'success')
            return redirect(url_for('admin_company.company_period'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while deleting the company entry: {str(e)}', 'danger')

    return render_template('admin/company/company_delete.html', form=form, company=company)


@admin_company_bp.route('/company_class_period/', methods=['GET', 'POST'])
@admin_required
def company_class_period():
    form = CompanyClassPeriodForm()  # 들여쓰기를 수정합니다.
    companies = []
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

                # company 테이블에서 지정된 기간 동안의 데이터를 조회하고 역순으로 정렬
                companies = Company.query.filter(
                    Company.register_date.between(start_date, end_date), Company.user_id == user_id
                ).order_by(Company.register_date.desc()).all()

                # 만약 특정 cost_class를 필터링하려는 경우

                if not companies:
                    flash('검색 결과가 없습니다.', 'warning')
                return render_template('admin/company/company_class_results.html',
                            companies=companies, company_class_choices=COMPANY_CLASS_CHOICES,
                                     enumerate=enumerate)
            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('admin/company/company_class_period.html', form=form)


"""
@admin_company_bp.route('/manage', methods=['GET'])
@admin_required
def manage_companies():
    user_id = session.get('user_id')        # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    companies = Company.query.filter(          # 모든 회사 항목 조회
        Company.user_id == user_id          # Cost.cost_date.between(start_date, end_date
    ).order_by(Company.register_date.desc()).all()

    # companies = Company.query.order_by(Company.register_date.desc()).all()  # 모든 회사 항목 조회
    return render_template('admin/company/manage_companies.html',
                companies=companies, company_class_choices=COMPANY_CLASS_CHOICES)
"""

