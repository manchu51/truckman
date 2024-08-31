from . import db
from datetime import datetime


class Question(db.Model):
    question_voter = db.Table(
        'question_voter',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
        db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
    )

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))


class Answer(db.Model):
    answer_voter = db.Table(
        'answer_voter',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
        db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
    )
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.Date, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    truck_name = db.Column(db.String(16))
    truck_no = db.Column(db.String(12), nullable=False)
    truck_class = db.Column(db.String(12))
    truck_ton = db.Column(db.Numeric(precision=3, scale=1), nullable=False)
    business_no = db.Column(db.String(12), nullable=False)
    company = db.Column(db.String(32), nullable=False)
    member_name = db.Column(db.String(16), nullable=False)
    zip = db.Column(db.String(6))
    address = db.Column(db.String(56))
    business_status = db.Column(db.String(16), nullable=False)
    business_item = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(64), unique=True)
    cellphone = db.Column(db.String(13), nullable=False)
    tel = db.Column(db.String(12))
    fax = db.Column(db.String(12))
    bank_name = db.Column(db.String(24))
    bank_no = db.Column(db.String(24))
    bank_account = db.Column(db.String(16))
    description = db.Column(db.String(32))


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

    # Example choices definition
    """
    위 코드에서 COST_CLASS_CHOICES와 PAYMENT_CHOICES는 중괄호 {} 로 둘러싸여 있어 
    set으로 인식됩니다. 그러나 실제로는 키 - 값 쌍으로 정의된 dictionary여야 합니다.
    """

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
        'C': '카드',
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



