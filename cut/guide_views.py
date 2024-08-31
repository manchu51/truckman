from flask import Blueprint, render_template

bp = Blueprint('guide', __name__, url_prefix='/guide')

@bp.route('/')
def show_guide():
    return render_template('guide.html')
