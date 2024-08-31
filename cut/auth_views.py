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
    return render_template('terms.html')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if form.validate_on_submit():
        # if request.method == 'POST' and form.validate_on_submit():
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

            # 로그인 성공 후 navbar.html로 이동

            return redirect(url_for('transport.create'))

            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))

        flash(error)
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


