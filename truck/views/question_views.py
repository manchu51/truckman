from datetime import datetime

from flask import Blueprint, render_template, jsonify, request, url_for, session, g, flash
from werkzeug.utils import redirect

from truck import db
from truck.models import Category, Question, Answer, User
from truck.forms import QuestionForm, AnswerForm
from truck.views.auth_views import login_required
import markdown
from markupsafe import Markup

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
@login_required
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    category_id = request.args.get('category_id', type=int, default=None)

    # 선택된 카테고리 가져오기 (없으면 None)
    category = Category.query.get(category_id) if category_id else None

    # 질문 리스트 필터링 (카테고리가 있을 경우)
    question_list = Question.query.order_by(Question.create_date.desc())

    if category:
        question_list = question_list.filter_by(category_id=category_id)

    # 검색어 필터링을 위한 함수
    def apply_search_filters(query, kw):
        if not kw:
            return query

        search = f'%{kw}%'
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()

        return query.join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(
            Question.subject.ilike(search) |
            Question.content.ilike(search) |
            User.username.ilike(search) |
            sub_query.c.content.ilike(search) |
            sub_query.c.username.ilike(search)
        ).distinct()

    # 검색어가 있을 경우 검색 적용
    question_list = apply_search_filters(question_list, kw)

    # 페이지네이션 처리 (필터링된 질문 리스트로)
    question_list = question_list.paginate(page=page, per_page=10)

    # 모든 카테고리 목록 가져오기
    categories = Category.query.all()

    # 템플릿에 question_list, categories, 선택된 category 전달
    return render_template(
        'question/question_list.html',
        question_list=question_list,
        categories=categories,
        category=category,      # 선택된 카테고리
        page=page,
        kw=kw
    )


@bp.route('/detail/<int:question_id>/')
@login_required
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    question_content_html = Markup(markdown.markdown(question.content))

    # 질문에 연결된 카테고리 가져오기
    category = question.category  # Question 모델에 category가 ForeignKey로 연결되어 있다고 가정

    return render_template('question/question_detail.html',
                           question=question,
                           content=question_content_html,
                           form=form,
                           category=category)  # 카테고리 정보 추가


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()

    # POST 요청일 경우
    if request.method == 'POST' and form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        category_id = request.form.get('category_id')  # category_id 가져오기

        # category_id 값이 없을 경우 처리
        if not category_id:
            flash('카테고리가 선택되지 않았습니다.')
            return redirect(url_for('question.create'))

        question = Question(
            subject=subject,
            content=content,
            user_id=g.user.id,
            create_date=datetime.now(),
            category_id=category_id  # 카테고리 설정
        )
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('question._list', category_id=category_id))

    # GET 요청일 경우
    category_id = request.args.get('category_id')  # URL에서 category_id 가져오기
    category = Category.query.get(category_id)

    return render_template('question/question_form.html', form=form, category=category)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))


@bp.route('/vote/<int:question_id>/', methods=['POST'])  # POST 요청으로 변경
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        return jsonify({'success': False, 'message': '본인이 작성한 글은 추천할 수 없습니다.'})
    else:
        _question.voter.append(g.user)
        db.session.commit()
        return jsonify({'success': True, 'voter_count': len(_question.voter)})


@bp.route('/partial')
def partial_question_list():
    category_id = request.args.get('category_id', type=int, default=None)
    if category_id:
        questions = Question.query.filter_by(category_id=category_id).all()
    else:
        questions = Question.query.all()

    return render_template('partials/question_list.html', question_list=questions)



"""
@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
    
    
@bp.route('/questions')
@login_required
def question_list():
    category_id = request.args.get('category_id', type=int, default=None)
    categories = Category.query.filter(Category.id.in_([4, 3, 2, 1, 0])).all()
    questions = get_questions_by_category(category_id)
    category = Category.query.get(category_id) if category_id else None
    return render_template('question/question_list.html', categories=categories, question_list=questions, category=category)




@bp.route('/detail/<int:question_id>/')
@login_required
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    question_content_html = Markup(markdown.markdown(question.content))
    return render_template('question/question_detail.html', question=question, content=question_content_html, form=form)


"""
