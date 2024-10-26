import functools

from datetime import datetime
from flask import Blueprint, url_for, render_template, redirect, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from truck import db
from truck.models import User
from truck.forms import UserCreateForm, UserLoginForm, CancelForm, UserModifyForm, UserForgotForm, UserResetForm
from flask_wtf.csrf import CSRFProtect
import logging

from flask import current_app
from truck import Mail
from truck.email import send_reset_email, get_reset_token

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/terms', methods=['GET'])
def terms():
    return render_template('auth/terms.html')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    truck_ton_value = form.truck_ton.data if form.truck_ton.data else 0
    email_value = form.email.data.strip() if form.email.data and form.email.data.strip() != '' else None

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            today = datetime.today().strftime("%Y-%m-%d")
            user = User(register_date=today,
                        username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        truck_name=form.truck_name.data,
                        truck_no=form.truck_no.data,
                        truck_class=form.truck_class.data,
                        truck_ton=truck_ton_value,
                        business_no=form.business_no.data,
                        company=form.company.data,
                        member_name=form.member_name.data,
                        zip=form.zip.data,
                        address=form.address.data,
                        business_status=form.business_status.data,
                        business_item=form.business_item.data,
                        email=email_value,
                        cellphone=form.cellphone.data,
                        tel=form.tel.data,
                        fax=form.fax.data,
                        bank_name=form.bank_name.data,
                        bank_no=form.bank_no.data,
                        bank_account=form.bank_account.data,
                        description=form.description.data)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            error = "존재하지 않는 회원입니다. 다시 로그인하여 주시기 바랍니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다. 다시 로그인하여 주시기 바랍니다."

        if error is None:
            session.clear()
            session['user_id'] = user.id
            #flash(f'Logged in user ID: {session["user_id"]}')

            # 세션 및 g.user 확인
            g.user = user  # g.user에 현재 로그인한 사용자 저장

            if user.is_admin:  # 관리자인 경우
                return redirect(url_for('admin.manage_users'))
            else:
                # `next` 매개변수를 사용해 안전한 리다이렉트 처리
                _next = request.args.get('next')
                if not _next or url_parse(_next).netloc != '':  # 안전한 리다이렉트 검사
                    _next = url_for('transport.create')
                return redirect(_next)

        flash(error)

    # 이 부분이 추가되었습니다. GET 요청 또는 폼 검증 실패 시, 로그인 페이지를 렌더링합니다.  *** 줄맞춤이 중요하다.
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):        # 사용자가 없거나, cancel_date가 있을 경우
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None or g.user.cancel_date is not None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


@bp.route('/member_modify/', methods=['GET', 'POST'])
@login_required
def member_modify():
    user = User.query.get(session['user_id'])  # 현재 로그인된 사용자 ID로 사용자 정보 가져오기
    form = UserModifyForm(obj=user)  # 사용자 데이터를 사용해 폼 초기화
    truck_ton_value = form.truck_ton.data if form.truck_ton.data else 0
    email_value = form.email.data.strip() if form.email.data is not None else None

    if form.validate_on_submit():
        # 사용자가 입력한 데이터를 user 객체에 한 번에 매핑
        fields = [
            'username', 'truck_name', 'truck_no', 'truck_class', 'truck_ton',
            'business_no', 'company', 'member_name', 'zip', 'address',
            'business_status', 'business_item', 'email', 'cellphone', 'tel',
            'fax', 'bank_name', 'bank_no', 'bank_account', 'description'
        ]

        for field in fields:
            setattr(user, field, getattr(form, field).data)  # form에서 값을 가져와 user 객체에 설정

        # 비밀번호 변경 시에만 업데이트
        if form.password1.data:
            user.password = generate_password_hash(form.password1.data)

        # 수정 날짜 설정
        user.modify_date = datetime.now()
        truck_ton = truck_ton_value
        email = email_value

        db.session.commit()  # 데이터베이스에 변경 사항 저장
        flash('회원 정보가 수정되었습니다.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/member_modify.html', user=user, form=form)


@bp.route('/member_cancel/', methods=['GET', 'POST'])
@login_required
def member_cancel():
    user_id = session.get('user_id')  # 현재 로그인된 사용자 ID 가져오기
    #form = CancelForm()

    if not user_id:
        flash("User is not logged in.")
        return redirect(url_for('auth.login'))

    # 탈퇴를 요청한 회원 id 가져오기
    user = User.query.get(session['user_id'])

    # 사용자가 해당 회원인지 확인
    if user.id != user_id:
        flash("You do not have permission to cancel this user entry.", 'danger')
        return redirect(url_for('main.index'))

    # 삭제 확인 폼
    form = CancelForm()

    # POST 요청 및 폼 유효성 검사
    if form.validate_on_submit():
        # user 테이블의 cancel_date에 현재 날짜를 입력
        user.cancel_date = datetime.now()  # 오늘 날짜로 cancel_date 설정
        db.session.commit()  # 변경사항을 DB에 저장
        flash('회원 탈퇴가 완료되었습니다.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/member_cancel.html', form=form, user=user)


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = UserForgotForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form['email']
        member_name = request.form['member_name']
        cellphone = request.form['cellphone']
        truck_no = request.form['truck_no']

        print(f"member_name: {member_name}, cellphone: {cellphone}, truck_no: {truck_no}")

        user = User.query.filter(
            #User.email == email,
            User.member_name == member_name,
            User.cellphone == cellphone,
            User.truck_no == truck_no,
        ).first()

        if user:
            # 입력 받은 이메일을 가져옴
            # email = request.form['email']

            # 유저 테이블의 email 칼럼에 입력받은 이메일을 업데이트
            user.email = email
            db.session.commit()  # 변경 사항을 DB에 저장

            #print(f"user: {user}")

            # 이메일을 업데이트한 후, 해당 이메일로 비밀번호 재설정 링크 전송
            token = get_reset_token(user.id)  # user.id를 사용하여 토큰 생성
            send_reset_email(user, token)

            flash('비밀번호 재설정 링크가 이메일로 발송되었습니다.', 'success')
            return redirect(url_for('auth.reset_password', token=token))

        else:
            flash('해당 정보를 가진 회원을 찾을 수 없습니다.', 'danger')

    return render_template('auth/forgot_password.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = UserResetForm()
    user = User.verify_token(token)  # verify_token에서 이미 User 객체를 반환하도록 수정

    if user is None:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('auth.forgot_password'))  # 토큰이 유효하지 않으면 리다이렉트
        print(f"user: {user}")  # user 출력해서 확인

    # 폼이 제출되었고 유효하면 비밀번호 변경 처리
    if form.validate_on_submit():
        new_password = form.password1.data
        user.set_password(new_password)  # 비밀번호 설정
        db.session.commit()  # 데이터베이스에 변경 사항 커밋
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))

    # 템플릿으로 폼 객체 전달
    return render_template('auth/reset_password.html', form=form, user=user, token=token)




