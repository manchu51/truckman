from functools import wraps

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
from truck import db
from truck.models import User, MembershipPayment
from truck.forms import PaymentCreateForm, PaymentPeriodForm, DeleteForm
from truck.views.admin_views import admin_required
from flask_wtf.csrf import CSRFProtect
import logging


admin_payment_bp = Blueprint('admin_payment', __name__, url_prefix='/admin/membership_payment')


@admin_payment_bp.route('/payment_create/', methods=['GET', 'POST'])
@admin_required
def payment_create():
    form = PaymentCreateForm()

    truck_no = request.form.get('truck_no')
    user = User.query.filter(
        User.truck_no == truck_no,
    ).first()

    if not user:
        flash("사용자를 찾을 수 없습니다.")
        return redirect(url_for('admin_payment.payment_create'))

    register_date = user.register_date

    # 가입일로부터 6개월 후 suspension_date 설정
    suspension_date = register_date + relativedelta(months=6)
    payment_amount = request.form.get('payment_amount')

    # 6개월이 지난 후 회비 부과 로직
    if datetime.now().date() > suspension_date:
        # 회비가 10,000원의 배수인지 확인
        monthly_fee = 10000
        months_to_extend = payment_amount // monthly_fee

        # suspension_date를 납부 금액에 따른 개월 수만큼 연장
        suspension_date = suspension_date + relativedelta(months=months_to_extend)

    if request.method == 'POST' and form.validate_on_submit():
        # 새로운 suspension_date 및 결제 정보를 저장
        new_payment = MembershipPayment(
            user_id=user.id,  # 이미 함수 내에서 user 객체를 가져왔으므로 user.id를 사용
            payment_date = request.form.get('payment_date'),
            payment_amount = payment_amount,
            suspension_date = suspension_date,
            annotation = request.form.get('annotation')
        )
        db.session.add(new_payment)
        db.session.commit()

        flash('회비결제가 성공적으로 입력 되었습니다.')
        #return redirect(url_for('admin_payment.payment_create'))

    #return render_template('admin/membership_payment/create_origin.html', form=form)



@admin_payment_bp.route('/payment_period', methods=['GET'])
@admin_required
def payment_period():
    form = PaymentPeriodForm()
    #querys = []
    payments = []

    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and form.validate_on_submit():
        # 검색 기간을 GET 요청에서 가져오기
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if start_date_str and end_date_str:
            try:
                # 문자열을 datetime 객체로 변환
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

                # 기본 쿼리 작성 (User 테이블과 조인, 결제 금액 합계 계산)
                query = db.session.query(
                    User.member_name,
                    User.truck_no,
                    MembershipPayment.payment_date.between(start_date, end_date),
                    func.sum(MembershipPayment.payment_amount).label('total_amount')
                ).join(User, MembershipPayment.user_id == User.id)

                if not query:
                    flash('검색 결과가 없습니다.', 'warning')

                return render_template('admin/membership_payment/list.html',
                            querys=querys, enumerate=enumerate, form=form)

            except ValueError:
                flash('잘못된 날짜 형식입니다.', 'danger')
        else:
            flash('날짜를 모두 입력하세요.', 'warning')

    # 검색 기간이 있을 경우 필터 추가
    if start_date and end_date:
        query = query.filter(MembershipPayment.payment_date.between(start_date, end_date))

    # 그룹화하여 회원별 총 결제 금액 계산
    query = query.group_by(User.id)

    # 쿼리 실행 및 결과 가져오기
    payments = query.all()

    # GET 요청일 경우 검색 폼을 렌더링
    return render_template('admin/membership_payment/list_period.html', form=form)



@admin_payment_bp.route('/payment_update/<int:id>', methods=['GET', 'POST'])
@admin_required
def payment_update(id):
    form = PaymentCreateForm(obj=payment)  # 결제 항목 데이터로 폼 초기화

    payment = membership_payment.query.get_or_404(id)

    if form.validate_on_submit():
        try:
            # 수정된 데이터 폼으로부터 가져와서 객체 필드에 일괄 적용
            form.populate_obj(payment)
            membership_payment.modify_date = datetime.now()  # 수정 날짜 업데이트

            db.session.commit()
            flash('MembershipPayment 결제가 성공적으로 수정되었습니다.', 'success')

            return redirect(url_for('admin_payment.payment_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the MembershipPayment entry: {str(e)}', 'danger')

    return render_template('admin/membership_payment/update.html', form=form, payment=payment)



@admin_payment_bp.route('/payment_delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def payment_delete(id):
    payment = MembershipPayment.query.get_or_404(id)

    form = DeleteForm()  # 삭제 확인 폼

    if form.validate_on_submit():
        try:
            db.session.delete(payment)
            db.session.commit()
            flash('결제가 성공적으로 삭제되었습니다.', 'success')

            return redirect(url_for('admin_payment.payment_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while deleting the cost entry: {str(e)}', 'danger')

    return render_template('admin/membership_payment/delete.html', payment=payment)


