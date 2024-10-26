from functools import wraps  # Import wraps

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from flask import Blueprint, url_for, render_template, flash, request, session, g
from truck.forms import PaymentCreateForm, PaymentPeriodForm, DeleteForm
from werkzeug.utils import redirect
from truck import db
from truck.models import User, Cost, Company, MembershipPayment
from truck.views.auth_views import login_required
from flask_wtf.csrf import CSRFProtect
import logging


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 관리자 권한 확인을 위한 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 로그인되지 않았거나 관리자가 아니면 로그인 페이지로 리디렉션
        if not session.get('user_id') or not g.get('is_admin', False):
            flash("관리자 권한이 필요합니다.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# 모든 요청에 대해 관리자인지 확인
@admin_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        g.is_admin = user and user.is_admin  # 관리자 여부 설정
    else:
        g.is_admin = False


# 관리자 대시보드
@admin_bp.route('/dashboard')
@admin_required
def dashboard():

    total_users = User.query.count()
    total_costs = Cost.query.count()
    new_register_today = User.query.filter(User.register_date == date.today()).count()
    total_revenue = Cost.query.with_entities(func.sum(Cost.cost_amount)).scalar() or 0

    return render_template(
        'admin/dashboard.html',
        user=User,
        username=session.get('username'),
        total_users=total_users,
        total_costs=total_costs,
        new_register_today=new_register_today,
        total_revenue=total_revenue
    )


@admin_bp.route('/admin/manage_users/', methods=['GET'])
@admin_required
def manage_users():
    # Logic for displaying and managing users
    today = datetime.today()            # 오늘 날짜
    fifteen_days_ago = today - timedelta(days=315)  # 오늘 날짜와 15일 이전 날짜 계산
    one_month_ago = today - timedelta(days=30)      # 오늘 날짜와 한 달 전 날짜 계산
    six_months_ago = today - timedelta(days=180)    # 오늘 날짜와 6개월 전 날짜 계산

    # URL 매개변수로부터 현재 페이지 가져오기, 기본값은 1
    page = request.args.get('page', 1, type=int)
    per_page = 20           # 한 페이지당 표시할 데이터 개수

    # User 테이블의 총 회원 수 계산
    total_users = User.query.count()

    # User와 MembershipPayment 조인, 6개월 이내 가입한 모든 회원 조회
    users_with_payment = (
        User.query
        .outerjoin(MembershipPayment, User.id == MembershipPayment.user_id)
        .filter(User.register_date >= six_months_ago)
        .add_columns(
            User.register_date.label('register_date'),
            User.username.label('username'),
            User.truck_no.label('truck_no'),
            User.member_name.label('member_name'),
            User.cellphone.label('cellphone'),
            User.address.label('address'),
            MembershipPayment.payment_date.label('payment_date'),
            MembershipPayment.payment_amount.label('payment_amount'),
            MembershipPayment.suspension_date.label('suspension_date')
        )
        .paginate(page=page, per_page=per_page)
    )

    return render_template(
        'admin/manage_users.html',
        users=users_with_payment,
        today=today,
        total_users=total_users,
        page=page,
        per_page=per_page
    )



@admin_bp.route('/admin/manage_costs/', methods=['GET'])
@admin_required
def manage_costs():
    costs = Cost.query.all()  # Admin can see all costs
    return render_template('admin/cost_form.html', costs=costs)



@admin_bp.route('/admin/payment_create/', methods=['GET', 'POST'])
@admin_required
def payment_create():
    form = PaymentCreateForm()

    # 오늘 날짜를 가져옵니다.
    today = datetime.today()

    # user 변수를 미리 None으로 초기화
    user = None
    payments = []

    if request.method == 'POST':
        truck_no = request.form.get('truck_no')
        print(f"Truck No: {truck_no}")  # 트럭 번호 출력으로 디버깅

        if not truck_no:
            flash("트럭 번호를 입력해 주세요.")
            return redirect(url_for('admin.payment_create'))

        # truck_no로 User를 쿼리
        user = User.query.filter(User.truck_no == truck_no).first()

        if not user:
            flash("사용자를 찾을 수 없습니다.")
            return redirect(url_for('admin.payment_create'))

        #print(f"User found: {user.username}")

        # 가입일(register_date) 안전하게 접근 후 처리
        register_date = user.register_date
        suspension_date = register_date + relativedelta(months=6)
        payment_amount = int(request.form.get('payment_amount', 0))  # 기본값 0 설정

        # 6개월 후 suspension_date 계산 및 회비 부과 처리
        if datetime.now().date() > suspension_date:
            monthly_fee = 10000  # 월 회비
            months_to_extend = payment_amount // monthly_fee

            # 납부 금액에 따라 suspension_date 연장
            suspension_date = suspension_date + relativedelta(months=months_to_extend)

        # 폼 검증 후 결제 정보 저장
        if form.validate_on_submit():
            new_payment = MembershipPayment(
                user_id=user.id,
                payment_date=request.form.get('payment_date'),
                payment_amount=payment_amount,
                suspension_date=suspension_date,
                annotation=request.form.get('annotation')
            )
            db.session.add(new_payment)
            db.session.commit()

            flash('회비 결제가 성공적으로 입력되었습니다.')
            return redirect(url_for('admin.payment_create'))

    # GET 요청일 경우, 기본 폼과 데이터를 렌더링
    if user:
        now_today = today.date()  # 오늘 날짜를 now_today로 설정
        payments = MembershipPayment.query.filter(
            MembershipPayment.payment_date == now_today,
            MembershipPayment.user_id == user.id
        ).all()
    else:
        payments = []  # user가 없을 경우 빈 리스트로 설정

    return render_template(
        'admin/payment_create_form.html',
        form=form,
        today=today,
        user=user,  # user 객체도 넘김
        payments=payments,
        enumerate=enumerate
    )



@admin_bp.route('/payment_period', methods=['GET', 'POST'])
@admin_required
def payment_period():
    form = PaymentPeriodForm()
    payments = []

    user_id = session.get('user_id')  # 현재 로그인된 관리자 ID 가져오기
    if not user_id:
        flash("User[관리자]가 로그인되지 않았습니다.", "danger")
        return redirect(url_for('auth.login'))

    # user_id로 User 객체 가져오기
    user = User.query.get(user_id)
    if not user or not user.is_admin:  # 관리자 여부 확인
        flash("관리자 권한이 없습니다.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if start_date and end_date:
            try:
                # 날짜 포맷 확인 및 변환
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

                # User와 MembershipPayment 테이블을 조인하고 결제 금액 합계를 계산하는 쿼리
                payments = db.session.query(
                    User.username,
                    User.register_date,
                    User.truck_no,
                    User.member_name,
                    MembershipPayment.id,  # id 추가
                    MembershipPayment.payment_date,  # payment_date 추가
                    MembershipPayment.payment_amount,
                    MembershipPayment.suspension_date,
                    MembershipPayment.annotation,
                    func.sum(MembershipPayment.payment_amount).label('total_amount')
                ).join(MembershipPayment, MembershipPayment.user_id == User.id) \
                    .filter(MembershipPayment.payment_date.between(start_date, end_date)) \
                    .group_by(User.id, MembershipPayment.id, MembershipPayment.payment_date).all()

                if not payments:
                    flash('검색 결과가 없습니다.', 'warning')

                return render_template('admin/payment_period_list.html',
                                       payments=payments, enumerate=enumerate)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('시작일과 종료일을 모두 입력하세요.', 'warning')

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('admin/payment_period.html', form=form)



@admin_bp.route('/payment_update/<int:id>', methods=['GET', 'POST'])
@admin_required
def payment_update(id):

    today = datetime.today()         # 오늘 날짜를 가져옵니다.
    # 특정 결제 항목을 데이터베이스에서 가져옵니다.
    payment = MembershipPayment.query.get_or_404(id)
    user = User.query.get(payment.user_id)  # 관련된 User 객체 가져오기

    # 결제 항목 데이터를 사용하여 폼을 초기화합니다.
    form = PaymentCreateForm(obj=payment)

    if form.validate_on_submit():
        try:
            # 수정된 데이터 폼으로부터 가져와서 객체 필드에 일괄 적용
            form.populate_obj(payment)
            payment.modify_date = datetime.now()  # 수정 날짜 업데이트

            db.session.commit()
            flash('MembershipPayment 결제가 성공적으로 수정되었습니다.', 'success')

            return redirect(url_for('admin.payment_period'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the MembershipPayment entry: {str(e)}', 'danger')

    return render_template('admin/payment_update.html', today=today, payment=payment, user=user, form=form)



@admin_bp.route('/payment_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def payment_delete(id):
    payment = MembershipPayment.query.get_or_404(id)

    form = DeleteForm()  # 삭제 확인 폼

    if form.validate_on_submit():
        try:
            db.session.delete(payment)
            db.session.commit()
            flash('결제가 성공적으로 삭제되었습니다.', 'success')

            return redirect(url_for('admin.payment_period'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while deleting the cost entry: {str(e)}', 'danger')

    return render_template('admin/payment_delete.html',form=form, payment=payment)










