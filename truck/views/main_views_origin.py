from flask import Blueprint, render_template, url_for, flash, request, redirect, session, g
from werkzeug.utils import redirect
from pybo.models import User
from pybo.forms import UserCreateForm, UserLoginForm

bp = Blueprint('main', __name__, url_prefix='/')
@bp.route('/')

def index():
   return render_template('index.html')

bp = Blueprint('auth', __name__, url_prefix='/auth')
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
                return redirect(url_for('main.index'))

        flash(error)
    return render_template('index.html', form=form)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        register_date=datetime.now(),
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



@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)






