from flask import render_template, redirect, url_for, flash
from truck import db
from truck.forms import LoginForm, SignupForm
from truck.models import User
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('auth/signup.html', form=form)


@bp.route('/terms')
def terms():
    return render_template('auth/terms.html')


@bp.route('/')
def index():
    return render_template('index.html')
