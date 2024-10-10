import functools
from sqlalchemy import func
from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.utils import redirect
from truck import db
from truck.models import Transport
from truck.forms import TransportForm, TransPeriodForm, TransSetPeriodForm, DeleteForm
from truck.views.auth_views import login_required
from flask_wtf.csrf import CSRFProtect
import logging
from math import ceil

TERMS_CHOICES = {
    'TP': '거래처선불',
    'TF': '거래처후불',
    'CP': '송하주선불',
    'CF': '송하주후불',
    'DP': '수하주선불',
    'DF': '수하주후불',
}

PAYMENT_CHOICES = {
    'E': '전자세금계산서',
    'P': '종이세금계산서',
    'S': '간이세금계산서',
    'C': '카드발급',
    'R': '간이영수증',
    'M': '현금영수증',
    'O': '기타',
}

bp = Blueprint('transport', __name__, url_prefix='/transport')


def empty_string_to_none(value):
    return value if value else None


@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = TransportForm()
    now_today = datetime.today().date()  # 오늘 날짜를 가져옵니다.
    today = datetime.today()
    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        # consignor가 없으면 trans_company 사용
        consignor = form.consignor.data or form.trans_company.data

        # 하차 일자가 없으면 운송 일자로 설정   [폼 데이터 가져오기]
        unload_date = request.form.get('unload_date')
        trans_date = request.form.get('trans_date')
        if not trans_date:
            trans_date = today
        if not unload_date:
            unload_date = trans_date

        # 거래처선불, 송하주선불, 수하주선불일 경우 운송료 입금일자를 운송일자로 대체함
        if form.terms.data in ['TP', 'CP', 'DP']:
            trans_set_date = form.trans_date.data
        else:                   # 조건을 만족하지 않으면 None으로 설정
            trans_set_date = None

        # 운송수수료가 있다면 운송수수료 지급일자를 운송일자로 대체함
        brokerage_fee = request.form.get('brokerage_fee')
        if brokerage_fee != '0':
            brokerage_date = trans_date
        else:                   # 조건을 만족하지 않으면 None으로 설정
            brokerage_date = None

        # trans_type = '부가가치세용' 이라면
        trans_type = request.form.get('trans_type')
        if trans_type == 'V':
            trans_set_date = trans_date,
            brokerage_date = trans_date

        transport = Transport(
            trans_date=form.trans_date.data,
            trans_company=form.trans_company.data,
            consignor=consignor,
            load_region=form.load_region.data,
            unload_date=unload_date,
            consignee=form.consignee.data,
            unload_region=form.unload_region.data,
            terms=form.terms.data,
            trans_amount=form.trans_amount.data,
            payment=form.payment.data,
            trans_set_date=trans_set_date,
            brokerage_fee=form.brokerage_fee.data
                        if form.brokerage_fee.data is not None else 0,  # 기본값 0
            brokerage_date=brokerage_date,
            trans_type=form.trans_type.data,
            comment=form.comment.data,
            user_id=user_id
        )

        db.session.add(transport)
        db.session.commit()
        flash(f'Transport table {form.trans_company.data} added successfully.')

        return redirect(url_for('transport.create', today=today))

    # 오늘 날짜로 입력된 모든 transport 데이터를 가져옵니다.
    transports = Transport.query.filter(
        Transport.trans_date == now_today, Transport.user_id == user_id
    ).all()

    return render_template('transport/transport_form.html',
            form=form, today=today, terms_choices=TERMS_CHOICES,
                    payment_choices=PAYMENT_CHOICES, transports=transports, enumerate=enumerate)


@bp.route('/trans_period/', methods=['GET', 'POST'])
@login_required
def trans_period():
    form = TransPeriodForm()
    view_type = request.args.get('view_type', 'transport')
    transports = []  # Initialize transports as an empty list
    today_date = datetime.now().strftime('%Y-%m-%d')  # Get current date

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        # POST 요청에서도 view_type 값을 받아옴
        view_type = request.form.get('view_type', view_type)

        if start_date and end_date:

            if view_type == 'transport':        # 운송 수정/삭제
                transports = Transport.query.filter(
                    Transport.trans_date.between(start_date, end_date),
                    Transport.trans_type == 'N',
                    Transport.user_id == user_id
                ).order_by(Transport.trans_date.desc()).all()

            elif view_type == 'unpaid':         # 전체 미수금현황
                transports = Transport.query.filter(
                    Transport.trans_date >= start_date,
                    Transport.trans_date <= end_date,
                    Transport.trans_set_date.is_(None),  # 미수금인 경우 trans_set_date가 None
                    Transport.trans_type == 'N',
                    Transport.user_id == user_id
                ).order_by(Transport.trans_date.desc()).all()

            elif view_type == 'transport_set':  # 전체 미수금 입금 현황
                transports = Transport.query.filter(
                    Transport.trans_date.between(start_date, end_date),
                    Transport.trans_set_date.isnot(None),  # 입금일자가 있는 경우
                    Transport.trans_type == 'N',
                    Transport.user_id == user_id
                ).order_by(Transport.trans_date.desc()).all()

            if not transports:
                flash('검색 결과가 없습니다.', 'warning')

            if view_type == 'transport':
                return render_template('transport/trans_period_results.html',
                        form=form, today_date=today_date, trans_company=trans_company,
                                transports=transports, terms_choices=TERMS_CHOICES,
                                    enumerate=enumerate)

            elif view_type == 'unpaid':
                return render_template('transport/trans_total_unpaid.html',
                        form=form, start_date=start_date, end_date=end_date,
                                today_date=today_date, transports=transports,
                                       terms_choices=TERMS_CHOICES, enumerate=enumerate)

            elif view_type == 'transport_set':
                return render_template('transport/trans_period_set_results.html',
                            form=form, today_date=today_date, transports=transports,
                                        terms_choices=TERMS_CHOICES, enumerate=enumerate)

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('transport/trans_period.html', form=form, view_type=view_type)


@bp.route('/trans_company/', methods=['GET', 'POST'])
@login_required
def trans_company():
    form = TransPeriodForm()
    view_type = request.args.get('view_type', 'company')
    transports = []  # Initialize transports as an empty list
    today_date = datetime.now().strftime('%Y-%m-%d')  # Get current date

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        trans_company = form.trans_company.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        #trans_company = request.form['trans_company']
        #start_date = request.form['start_date']
        #end_date = request.form['end_date']
        # POST 요청에서도 view_type 값을 받아옴
        view_type = request.form.get('view_type', view_type)

        if start_date and end_date:
            try:
                #start_date = datetime.strptime(start_date, '%Y-%m-%d')
                #end_date = datetime.strptime(end_date, '%Y-%m-%d')

                if view_type == 'company':          # 거래처 운송현황
                    transports = Transport.query.filter(
                        Transport.trans_company == trans_company,
                        Transport.trans_date >= start_date,
                        Transport.trans_date <= end_date,
                        Transport.trans_type == 'N',
                        Transport.user_id == user_id
                    ).order_by(Transport.trans_date.desc()).all()

                elif view_type == 'unpaid':         # 거래처 미수금 현황
                    transports = Transport.query.filter(
                        Transport.trans_company == trans_company,
                        Transport.trans_date >= start_date,
                        Transport.trans_date <= end_date,
                        Transport.trans_set_date.is_(None),  # 미수금인 경우 trans_set_date가 None
                        Transport.trans_type == 'N',
                        Transport.user_id == user_id
                    ).order_by(Transport.trans_date.desc()).all()

                elif view_type == 'set':         # 거래처 미수금 입금
                    transports = Transport.query.filter(
                        Transport.trans_company == trans_company,
                        Transport.trans_date >= start_date,
                        Transport.trans_date <= end_date,
                        Transport.terms == 'TF',
                        Transport.trans_set_date.is_(None),  # 미수금인 경우 trans_set_date가 None
                        Transport.trans_type == 'N',
                        Transport.user_id == user_id
                    ).order_by(Transport.trans_date.desc()).all()

                elif view_type == 'company_set':          # 거래처 미수금 입금현황
                    transports = Transport.query.filter(
                        Transport.trans_company == trans_company,
                        Transport.trans_date >= start_date,
                        Transport.trans_date <= end_date,
                        Transport.trans_set_date.is_not(None),
                        Transport.trans_type == 'N',
                        Transport.user_id == user_id
                    ).order_by(Transport.trans_date.desc()).all()

                if not transports:
                    flash('검색 결과가 없습니다.', 'warning')

                if view_type == 'company':
                    return render_template('transport/trans_company_results.html',
                        form=form, trans_company=trans_company, transports=transports,
                                terms_choices=TERMS_CHOICES, enumerate=enumerate)
                elif view_type == 'unpaid':
                    return render_template('transport/trans_unpaid_results.html',
                        form=form, today_date=today_date, trans_company=trans_company,
                                start_date=start_date, end_date = end_date,
                                        transports=transports, terms_choices=TERMS_CHOICES,
                                           enumerate=enumerate)
                elif view_type == 'set':
                    return render_template('transport/trans_company_set.html',
                            form=form, trans_company=trans_company, today_date=today_date,
                                    transports=transports,
                                           terms_choices=TERMS_CHOICES, enumerate=enumerate)

                elif view_type == 'company_set':
                    return render_template('transport/trans_company_set_results.html',
                            form=form, trans_company=trans_company, today_date=today_date,
                                    transports=transports,
                                           terms_choices=TERMS_CHOICES, enumerate=enumerate)
            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('transport/trans_company.html', form=form, view_type=view_type)


@bp.route('/trans_set_period/', methods=['GET', 'POST'])
@login_required
def trans_set_period():
    form = TransSetPeriodForm()
    transports = []  # Initialize transports as an empty list

    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        start_date = form.start_date.data
        end_date = form.end_date.data

        if start_date and end_date:
            try:
                transports = Transport.query.filter(
                    Transport.trans_date.between(start_date, end_date),
                    Transport.trans_set_date.is_(None),  # 미수금인 경우 trans_set_date가 None == None
                    Transport.user_id == user_id
                ).order_by(Transport.trans_date.desc()).all()

                if not transports:
                    flash('검색 결과가 없습니다.', 'warning')

                # Render the results page with the transports data
                return render_template('transport/trans_update_set.html',
                            form=form, transports=transports, enumerate=enumerate)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    # Always render the form for GET requests or if POST validation fails
    return render_template('transport/trans_set_period.html', form=form)


@bp.route('/trans_update_set/', methods=['GET', 'POST'])
@login_required
def trans_update_set():
    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Iterate through the list of transports and update the trans_set_date
        for transport in Transport.query.all():
            trans_set_date_field = f'trans_set_date_{transport.id}'
            trans_set_date = request.form.get(trans_set_date_field)
            if trans_set_date:
                try:
                    transport.trans_set_date = datetime.strptime(trans_set_date, '%Y-%m-%d')
                except ValueError:
                    flash(f'Invalid date format for transport ID {transport.id}', 'danger')
                else:
                    transport.trans_set_date = datetime.strptime(trans_set_date, '%Y-%m-%d')

        db.session.commit()
        flash('미수금 내역이 성공적으로 저장되었습니다.', 'success')

        # Handling GET request to redirect appropriately
        return redirect(url_for('transport.trans_set_period'))



@bp.route('/trans_modify/<int:id>', methods=['GET', 'POST'])
@login_required
def trans_modify(id):
    transport = Transport.query.get_or_404(id)   # 데이터베이스에서 해당 id를 가진 Transport 객체를 가져옵니다.
    user_id = session.get('user_id')  # 로그인된 사용자 ID

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    # 디버깅 출력: user_id와 transport.user_id 확인
    # print(f"user_id: {user_id}, transport.user_id: {transport.user_id}")

    # 사용자가 수정할 권한이 있는지 확인
    if transport.user_id != user_id:
        flash("You do not have permission to modify this transport entry.", 'danger')
        return redirect(url_for('transport.trans_period'))

    form = TransportForm(obj=transport)  # Transport 객체로부터 초기값 설정

    if form.validate_on_submit():
        form.populate_obj(transport)  # 폼 데이터를 Transport 객체에 반영
        transport.modify_date = datetime.now()  # 수정일 갱신
        db.session.commit()
        flash('운송 정보가 수정 되었습니다.', 'success')
        return redirect(url_for('transport.trans_period'))  # 수정 후 리디렉션할 URL을 지정

    return render_template('transport/trans_modify.html', form=form, transport=transport)


@bp.route('/trans_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def trans_delete(id):
    transport = Transport.query.get_or_404(id)      # 삭제할 운송 항목 가져오기
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    # 로그인된 사용자가 없으면 로그인 페이지로 리디렉션
    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    # 디버깅 출력: user_id와 transport.user_id 확인
    # print(f"user_id: {user_id}, transport.user_id: {transport.user_id}")

    # 사용자가 해당 운송 항목의 소유자인지 확인
    if transport.user_id != user_id:  # transport 객체의 user_id와 비교
        flash("You do not have permission to delete this transport entry.", 'danger')
        return redirect(url_for('transport.trans_period'))

    form = DeleteForm()  # 삭제 확인 폼

    if form.validate_on_submit():  # POST 요청 및 폼 유효성 검사
        db.session.delete(transport)  # 해당 transport 객체 삭제
        db.session.commit()
        flash('운송 정보가 삭제되었습니다.', 'success')
        return redirect(url_for('transport.trans_period'))

    # GET 요청 시 삭제 확인 페이지 렌더링
    return render_template('transport/trans_delete.html', form=form, transport=transport)


@bp.route('/trans_company_set/', methods=['GET', 'POST'])
@login_required
def trans_company_set():
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    form = TransPeriodForm()
    view_type = request.args.get('view_type', 'set')
    if request.method == 'POST':
        # Iterate through the list of transports and update the trans_set_date
        for transport in Transport.query.all():
            trans_set_date_field = f'trans_set_date_{transport.id}'
            trans_set_date = request.form.get(trans_set_date_field)
            if trans_set_date:
                try:
                    transport.trans_set_date = datetime.strptime(trans_set_date, '%Y-%m-%d')
                except ValueError:
                    flash(f'Invalid date format for transport ID {transport.id}', 'danger')
                else:
                    transport.trans_set_date = datetime.strptime(trans_set_date, '%Y-%m-%d')

        db.session.commit()
        flash('미수금 내역이 성공적으로 저장되었습니다.', 'success')

        return redirect(url_for('transport.trans_company'))

    # Handling GET request to redirect appropriately
    return render_template('transport/trans_company.html', form=form, view_type=view_type)

# Example data for pagination
@bp.route('/total_unpaid_print', methods=['GET'])
@login_required
def total_unpaid_print(page=1, per_page=15):
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    today_date = datetime.now().strftime('%Y-%m-%d')  # Get current date
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # 로그로 start_date와 end_date 출력
    logging.debug(f"start_date: {start_date}, end_date: {end_date}")

    # start_date와 end_date가 존재하지 않으면, 기본값을 설정하거나 오류를 처리
    if not start_date or not end_date:
        # 기본값 설정 또는 오류 처리
        return "first_date와 last_date가 필요합니다.", 400

    # start_date와 end_date로 필터링된 쿼리 생성
    filtered_transports = db.session.query(
        Transport.trans_company,
        Transport.terms,
        db.func.min(Transport.trans_date).label('trans_date'),  # 각 그룹 내 최소 운송일자
        db.func.min(Transport.consignor).label('consignor'),
        db.func.min(Transport.consignee).label('consignee'),
        db.func.min(Transport.load_region).label('load_region'),
        db.func.min(Transport.unload_region).label('unload_region'),
        db.func.count(Transport.id).label('count'),
        db.func.sum(Transport.trans_amount).label('total_amount'),
        db.func.sum(Transport.brokerage_fee).label('total_fee'),

    ).filter(
        Transport.trans_date.between(start_date, end_date),
        Transport.trans_set_date.is_(None),
        Transport.trans_type == 'N',
        Transport.user_id == user_id
    ).group_by(
        Transport.trans_company, Transport.terms).all()

    # Calculate total number of pages
    total_count = len(filtered_transports)
    total_pages = ceil(total_count / per_page)

    # Paginate the transports list
    start = (page - 1) * per_page
    end = start + per_page
    paginated_transports = filtered_transports[start:end]

    # 결과를 렌더링할 템플릿으로 전달
    return render_template('transport/total_unpaid_print.html',
            today_date=today_date, start_date=start_date, end_date = end_date,
                    transports=paginated_transports, page=page, total_pages=total_pages)

# Example data for pagination
@bp.route('/company_unpaid_print', methods=['GET'])
@login_required
def company_unpaid_print(page=1, per_page=15):
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    today_date = datetime.now().strftime('%Y-%m-%d')  # Get current date
    trans_company = request.args.get('trans_company')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # 로그로 start_date와 end_date 출력
    logging.debug(f"start_date: {start_date}, end_date: {end_date}")

    # start_date와 end_date가 존재하지 않으면, 기본값을 설정하거나 오류를 처리
    if not start_date or not end_date:
        # 기본값 설정 또는 오류 처리
        return "first_date와 last_date가 필요합니다.", 400

    filtered_transports = Transport.query.filter(
        Transport.trans_company == trans_company,
        Transport.trans_date >= start_date,
        Transport.trans_date <= end_date,
        Transport.trans_set_date.is_(None),  # 미수금인 경우 trans_set_date가 None
        Transport.trans_type == 'N',
        Transport.user_id == user_id
    ).order_by(Transport.trans_date.desc()).all()

    # Calculate total number of pages
    total_count = len(filtered_transports)
    total_pages = ceil(total_count / per_page)

    # Paginate the transports list
    start = (page - 1) * per_page
    end = start + per_page
    paginated_transports = filtered_transports[start:end]

    # 결과를 렌더링할 템플릿으로 전달
    return render_template('transport/company_unpaid_print.html',
            today_date=today_date, start_date=start_date, end_date=end_date,
                    trans_company=trans_company, transports=paginated_transports,
                           page=page, total_pages=total_pages)

