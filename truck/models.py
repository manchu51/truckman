from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from . import db

# 중간 테이블 정의 (Question 및 Answer의 추천 기능을 위한 테이블)
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

# 카테고리 모델 정의
class Category(db.Model):
    __tablename__ = 'category'  # 테이블 이름이 일치해야 함
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'

# 질문 모델 정의
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    modify_date = db.Column(db.DateTime(), nullable=True)
    # 사용자 및 추천 기능
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

    user = db.relationship('User', backref=db.backref('question_set'))
    category = db.relationship('Category', backref=db.backref('question_set'))

    def __repr__(self):
        return f'<Question {self.subject}>'

# 답변 모델 정의
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    modify_date = db.Column(db.DateTime(), nullable=True)

    # 질문과 답변 간의 관계
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))

    # 사용자 및 추천 기능
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

    def __repr__(self):
        return f'<Answer {self.content[:15]}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.Date, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    cancel_date = db.Column(db.DateTime(), nullable=True)
    deposit_date = db.Column(db.DateTime(), nullable=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    truck_name = db.Column(db.String(16))
    truck_no = db.Column(db.String(12), nullable=False)
    truck_class = db.Column(db.String(12))
    truck_ton = db.Column(db.Numeric(precision=3, scale=1), nullable=True)
    business_no = db.Column(db.String(12), nullable=False)
    company = db.Column(db.String(32), nullable=False)
    member_name = db.Column(db.String(16), nullable=False)
    zip = db.Column(db.String(6))
    address = db.Column(db.String(56))
    business_status = db.Column(db.String(16), nullable=False)
    business_item = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=True)    # nullable=True로 설정
    cellphone = db.Column(db.String(13), nullable=False)
    tel = db.Column(db.String(12))
    fax = db.Column(db.String(12))
    bank_name = db.Column(db.String(24))
    bank_no = db.Column(db.String(24))
    bank_account = db.Column(db.String(16))
    description = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean, default=False)

    payments = db.relationship('MembershipPayment', backref='user', lazy=True)

    @staticmethod
    def verify_token(token):
        """토큰 검증 후 사용자 반환"""
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 토큰 디코딩
            user_id = data.get('user_id')  # 'user_id'로 저장한 값을 추출
            #print(f"Decoded user_id: {user_id}")  # user_id 출력해서 확인
        except:
            return None  # 토큰이 유효하지 않거나 만료됨

        return User.query.get(user_id)

    # 비밀번호 설정 메서드
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 비밀번호 검증 메서드
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MembershipPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User와의 관계
    payment_date = db.Column(db.Date, nullable=False)  # 회비 입금일자
    payment_amount = db.Column(db.Integer, nullable=False)  # 입금금액
    suspension_date = db.Column(db.Date, nullable=True)  # 정지일자 (가입일자 + 6개월)
    modify_date = db.Column(db.DateTime(), nullable=True)
    annotation = db.Column(db.String(32))


class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trans_date = db.Column(db.Date, nullable=True)
    modify_date = db.Column(db.DateTime(), nullable=True)
    trans_company = db.Column(db.String(32), nullable=True)
    consignor = db.Column(db.String(32), nullable=True)
    load_region = db.Column(db.String(64), nullable=True)
    unload_date = db.Column(db.Date, nullable=True)
    consignee = db.Column(db.String(32), nullable=True)
    unload_region = db.Column(db.String(64), nullable=True)
    terms = db.Column(db.String(2), nullable=False)
    trans_amount = db.Column(db.Integer, nullable=False)
    payment = db.Column(db.String(1), nullable=True)
    trans_set_date = db.Column(db.Date, nullable=True)
    brokerage_fee = db.Column(db.Integer, nullable=True)
    brokerage_date = db.Column(db.Date, nullable=True)
    trans_type = db.Column(db.String(1), nullable=False)
    comment = db.Column(db.String(32), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)


class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost_date = db.Column(db.Date, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    cost_company = db.Column(db.String(32), nullable=False)
    cost_class = db.Column(db.String(1), nullable=False)
    statement = db.Column(db.String(32))
    payment = db.Column(db.String(1), nullable=False)
    bank_card = db.Column(db.String(32))
    cost_amount = db.Column(db.Integer)
    memo = db.Column(db.String(32), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    COST_CLASS_CHOICES = {
        'D': '경유',
        'G': '휘발유',
        'E': '전기충전',
        'T': '차량관리',
        'N': '생필품',
        'M': '식대',
        'F': '면세품목',
        'O': '기타'
    }

    PAYMENT_CHOICES = {
        'E': '전자세금계산서',
        'P': '종이세금계산서',
        'S': '간이세금계산서',
        'C': '카드발급',
        'R': '간이영수증',
        'M': '현금영수증',
        'O': '기타'
    }


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.Date, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    company_class = db.Column(db.String(1), nullable=False)
    business_no = db.Column(db.String(12), nullable=False)
    firm = db.Column(db.String(32), nullable=False)
    president = db.Column(db.String(16), nullable=True)
    zip = db.Column(db.String(6))
    address = db.Column(db.String(56))
    business_status = db.Column(db.String(16), nullable=True)
    business_item = db.Column(db.String(16), nullable=True)
    email = db.Column(db.String(64))
    cellphone = db.Column(db.String(13), nullable=True)
    tel = db.Column(db.String(12))
    fax = db.Column(db.String(12))
    note = db.Column(db.String(32), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)




