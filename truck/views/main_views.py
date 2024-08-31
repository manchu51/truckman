from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from truck.forms import UserLoginForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    form = UserLoginForm()
    return render_template('index.html', form=form)


