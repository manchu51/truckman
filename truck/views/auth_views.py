import functools

from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from truck import db
from truck.forms import UserCreateForm, UserLoginForm
from truck.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/terms', methods=['GET'])
def terms():
    #return render_template('terms.html')
    return render_template('auth/terms.html')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
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
                        truck_ton=form.truck_ton.data,
                        business_no=form.business_no.data,
                        company=form.company.data,
                        member_name=form.member_name.data,
                        zip=form.zip.data,
                        address=form.address.data,
                        business_status=form.business_status.data,
                        business_item=form.business_item.data,
                        email=form.email.data,
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
        else:
            flash('이미 존재하는 회원입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            error = "존재하지 않는 회원입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."

        if error is None:
            session.clear()
            session['user_id'] = user.id

            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                # 로그인 성공 후 특정 페이지로 리다이렉트
                return redirect(url_for('transport.create'))

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


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


@bp.route('/member_modify/', methods=['GET', 'POST'])
@login_required
def member_modify():
    #user = User.query.get(current_user.id)  # Get the current logged-in user from the database
    user = User.query.get(session['user_id'])
    form = UserCreateForm(obj=user)  # Populate the form with the current user's data

    if form.validate_on_submit():
        user.username = form.username.data
        if form.password1.data:
            user.password = generate_password_hash(form.password1.data)

        user.truck_name = form.truck_name.data
        user.truck_no = form.truck_no.data
        user.truck_class = form.truck_class.data
        user.truck_ton = form.truck_ton.data
        user.business_no = form.business_no.data
        user.company = form.company.data
        user.member_name = form.member_name.data
        user.zip = form.zip.data
        user.address = form.address.data
        user.business_status = form.business_status.data
        user.business_item = form.business_item.data
        user.email = form.email.data
        user.cellphone = form.cellphone.data
        user.tel = form.tel.data
        user.fax = form.fax.data
        user.bank_name = form.bank_name.data
        user.bank_no = form.bank_no.data
        user.bank_account = form.bank_account.data
        user.description = form.description.data

        user.modify_date = datetime.now()

        db.session.commit()
        flash('회원 정보가 수정되었습니다.')
        return redirect(url_for('main.index'))

    return render_template('auth/member_modify.html', user=user, form=form)

