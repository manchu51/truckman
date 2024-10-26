from datetime import datetime

from flask import Blueprint, url_for, request, render_template, jsonify, session, g, flash
from werkzeug.utils import redirect

from truck import db
from ..forms import AnswerForm
from truck.models import Category, Question, Answer, User
from .auth_views import login_required
import markdown
from markupsafe import Markup

bp = Blueprint('answer', __name__, url_prefix='/answer')

"""
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    # 페이지 번호를 URL 매개변수로부터 받음, 기본값은 1
    page = request.args.get('page', type=int, default=1)

    # 답변을 페이징 처리하여 5개씩 출력
    answers = question.answer_set.order_by(Answer.create_date.asc()).paginate(page, per_page=5)

    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()

        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id, page=page), answer.id))

    return render_template('question/question_detail.html', question=question, answers=answers, form=form)
"""

@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user, question_id=question_id)
        db.session.add(answer)
        db.session.commit()

        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))

    # Answer 모델에 대해 직접 쿼리를 수행하여 정렬 및 페이징
    page = request.args.get('page', type=int, default=1)
    answers = Answer.query.filter_by(question_id=question.id)\
                          .order_by(Answer.create_date.asc())\
                          .paginate(page, per_page=5)

    return render_template('question/question_detail.html', question=question, answers=answers, form=form)



@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))

    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()

            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)

    return render_template('answer/answer_form.html', form=form)


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))


@bp.route('/vote/<int:answer_id>/', methods=['POST'])  # POST 요청으로 처리
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        return jsonify({'success': False, 'message': '본인이 작성한 글은 추천할 수 없습니다.'})
    else:
        _answer.voter.append(g.user)
        db.session.commit()
        return jsonify({'success': True, 'voter_count': len(_answer.voter)})

"""
@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()

    return redirect('{}#answer_{}'.format(
        url_for('question.detail', question_id=answer.question.id), answer.id))

"""

