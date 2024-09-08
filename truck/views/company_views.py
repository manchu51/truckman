from datetime import datetime
from datetime import date

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from flask_wtf.csrf import CSRFProtect

from .. import db
from truck.models import Company, User
from truck.forms import CompanyForm, CompanyPeriodForm, DeleteForm, CompanyClassPeriodForm

from truck.views.auth_views import login_required

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

    if request.method == 'POST' and form.validate_on_submit():
        company = Company(register_date=form.register_date.data, company_class=form.company_class.data,
            business_no=form.business_no.data, firm=form.firm.data, president=form.president.data,
                zip=form.zip.data, address=form.address.data, business_status=form.business_status.data,
                    business_item=form.business_item.data, email=form.email.data, cellphone=form.cellphone.data,
                        tel=form.tel.data, fax=form.fax.data,  note=form.note.data)

        db.session.add(company)
        db.session.commit()
        flash(f'Company table {form.firm.data} added successfully.')
        # flash('Company Table added successfully.')
        return redirect(url_for('company.create', today=today))

    # 오늘 날짜로 입력된 모든 transport 데이터를 가져옵니다.
    companies = Company.query.filter(
        Company.register_date == now_today
    ).all()

    return render_template('company/company_form.html', form=form, today=today,
                companies=companies, enumerate=enumerate)


@bp.route('/company_period', methods=['GET', 'POST'])
def company_period():
    form = CompanyPeriodForm()
    companies = []
    if request.method == 'POST' and form.validate_on_submit():
        start_date = request. form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                companies = Company.query.filter(
                    Company.register_date.between(start_date, end_date)
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

    if form.validate_on_submit():
        form.populate_obj(company)  # 폼 데이터를 Company 객체에 반영
        db.session.commit()
        flash('업체 정보가 수정되었습니다.', 'success')
        return redirect(url_for('company.company_period'))

    return render_template('company/company_modify.html', form=form, company=company)


@bp.route('/delete_company/<int:company_id>', methods=['GET', 'POST'])
@login_required
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    form = DeleteForm()
    if request.method == 'POST':
        db.session.delete(company)
        db.session.commit()
        flash('Company deleted successfully.')
        return redirect(url_for('company.company_period'))
    return render_template('company/company_delete.html', form=form, company=company)


@bp.route('/company_class_period', methods=['GET', 'POST'])
@login_required
def company_class_period():
    form = CompanyClassPeriodForm()  # 들여쓰기를 수정합니다.
    companies = None

    if request.method == 'POST' and form.validate_on_submit():
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                # company 테이블에서 지정된 기간 동안의 데이터를 조회하고 역순으로 정렬
                companies = Company.query.filter(
                    Company.register_date >= start_date,
                    Company.register_date <= end_date
                ).order_by(Company.register_date.desc()).all()

                # 만약 특정 cost_class를 필터링하려는 경우

                if not companies:
                    flash('검색 결과가 없습니다.', 'warning')
                return render_template('company/company_class_results.html',
                            companies=companies, company_class_choices=COMPANY_CLASS_CHOICES,
                                     enumerate=enumerate)            # COMPANY_CLASS_CHOICES

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('company/company_class_period.html', form=form)
