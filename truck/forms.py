from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, DecimalField, TextAreaField, PasswordField,
                     EmailField, SelectField, IntegerField, FloatField, SubmitField)
from wtforms.validators import (DataRequired, Length, Regexp, EqualTo, Email, ValidationError,
                                NumberRange, Optional)
from .models import User

def cellphone_field():
    return StringField(
        '핸드폰 번호',
        validators=[
            DataRequired(),
            Length(min=13, max=13),
            Regexp(r'^010-\d{4}-\d{4}$', message="핸드폰번호 형식은 010-8888-7777 이어야 합니다.")
        ]
    )

def tel_field():
    return StringField(
        '전화 번호',
        validators=[
            Optional(),  # 입력 생략 가능
            Length(min=12, max=12),
            Regexp(r'^051-\d{3}-\d{4}$', message="전화번호 형식은 051-333-5555 이어야 합니다.")
        ]
    )

def fax_field():
    return StringField(
        '팩스 번호',
        validators=[
            Optional(),  # 입력 생략 가능
            Length(min=12, max=12),
            Regexp(r'^051-\d{3}-\d{4}$', message="팩스번호 형식은 051-333-5555 이어야 합니다.")
        ]
    )

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    username = StringField('회원아이디', validators=[DataRequired(), Length(min=2, max=12)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), Length(min=3, max=12), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    truck_name = StringField('트럭명칭')
    truck_no = StringField('트럭번호', validators=[DataRequired('트럭번호는 필수입력 항목입니다.')])
    truck_class = StringField('트럭종류')
    truck_ton = DecimalField('트럭 톤수', places=1, validators=[Optional()])  # 입력 생략 가능
    business_no = StringField('사업자등록번호')
    company = StringField('회사명')
    member_name = StringField('회원이름', validators=[DataRequired(), Length(min=2, max=12)])
    zip = StringField('우편번호')
    address = StringField('주소')
    business_status = StringField('업태')
    business_item = StringField('종목')
    email = StringField('Email', validators=[Optional(), Email()])
    cellphone = cellphone_field()  # 공통 핸드폰 번호 필드를 사용
    tel = tel_field()
    fax = fax_field()
    bank_name = StringField('은행명')
    bank_no = StringField('계좌번호')
    bank_account = StringField('소유자이름')
    description = StringField('비고')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('이미 존재하는 회원이름입니다. 다른 이름을 사용하여 주십시요.')

    def validate_email(self, field):
        if field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError('이미 등록된 Email 입니다. 정확한 Email 을 등록하여 주십시요.')

class UserLoginForm(FlaskForm):
    username = StringField('회원아이디', validators=[DataRequired(), Length(min=2, max=12)])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

class UserForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    member_name = StringField('회원 이름', validators=[DataRequired(), Length(min=2, max=12)])
    cellphone = cellphone = cellphone_field()  # 함수를 호출하여 필드 할당StringField(
    truck_no = StringField('트럭 번호', validators=[DataRequired()])
    submit = SubmitField('비밀번호 재설정')

class TransportForm(FlaskForm):
    trans_date = DateField('운송 일자', format='%Y-%m-%d', validators=[DataRequired()])
    trans_company = StringField('거래처', validators=[DataRequired()])
    consignor = StringField('송하주')
    load_region = StringField('상차지')
    unload_date = DateField('하차 일자', format='%Y-%m-%d', validators=[Optional()])  # Optional validator 추가
    consignee = StringField('수하주')
    unload_region = StringField('하차지')
    terms = SelectField('거래 조건', choices=[
        ('TP', '거래처선불'),
        ('TF', '거래처후불'),
        ('CP', '송하주선불'),
        ('CF', '송하주후불'),
        ('DP', '수하주선불'),
        ('DF', '수하주후불'),
    ], validators=[DataRequired()], default='TF')
    trans_amount = IntegerField('운송료', validators=[DataRequired(), NumberRange(min=10000, max=5000000)])
    payment = SelectField('거래 방법', choices=[
        ('E', '전자세금계산서'),
        ('P', '종이세금계산서'),
        ('S', '간이세금계산서'),
        ('C', '카드발급'),
        ('R', '간이영수증'),
        ('M', '현금영수증'),
        ('O', '기타')
    ], validators=[DataRequired()])
    trans_set_date = DateField('운송 입금 일자', format='%Y-%m-%d', validators=[Optional()])
    brokerage_fee = IntegerField('운송 수수료', default=0, validators=[Optional()])
    brokerage_date = DateField('수수료 송금 일자', format='%Y-%m-%d', validators=[Optional()])
    trans_type = SelectField('거래 형태', choices=[
        ('N', '정상거래'),
        ('V', '부가가치세용')
    ])
    comment = StringField('비고', validators=[Optional()])


class CostForm(FlaskForm):
    cost_date = DateField('경비 일자', format='%Y-%m-%d', validators=[DataRequired()])
    cost_company = StringField('회사명', validators=[DataRequired()])
    cost_class = SelectField('경비 형태', choices=[
        ('D', '경유'),
        ('G', '휘발유'),
        ('E', '전기충전'),
        ('T', '차량관리'),
        ('N', '생필품'),
        ('M', '식대'),
        ('F', '면세품목'),
        ('O', '기타')
    ], validators=[DataRequired()])
    statement = StringField('거래 내역', validators=[Optional()])
    payment = SelectField('거래 방법', choices=[
        ('E', '전자세금계산서'),
        ('P', '종이세금계산서'),
        ('S', '간이세금계산서'),
        ('C', '카드'),
        ('R', '간이영수증'),
        ('M', '현금영수증'),
        ('O', '기타')
    ], validators=[DataRequired()])
    bank_card = StringField('카드 은행', validators=[Optional()])
    cost_amount = DecimalField('금액', validators=[DataRequired()])
    memo = StringField('비고', validators=[Optional()])


class CompanyForm(FlaskForm):
    register_date = DateField('등록 일자', format='%Y-%m-%d', validators=[DataRequired()])
    company_class = SelectField('회사 분류', choices=[
        ('R', '매출처'),       # Revenue
        ('P', '매입처')        # Purchase
    ], validators=[DataRequired()])
    business_no = StringField('사업자등록번호', validators=[DataRequired('사업자등록번호는 필수입력 항목입니다.')])
    firm = StringField('회사명', validators=[DataRequired('회사명은 필수입력 항목입니다.')])
    president = StringField('대표자 성명', validators=[Optional()])
    zip = StringField('우편번호', validators=[Optional()])
    address = StringField('주소', validators=[Optional()])
    business_status = StringField('업태', validators=[Optional()])
    business_item = StringField('종목', validators=[Optional()])
    email = StringField('이메일', validators=[Optional()])
    cellphone = cellphone_field()  # 공통 핸드폰 번호 필드를 사용
    tel = StringField('전화번호', validators=[Optional()])
    fax = StringField('fax 번호', validators=[Optional()])
    note = StringField('비고', validators=[Optional()])


class TransPeriodForm(FlaskForm):
    trans_company = StringField('거래처', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class ConsignTransPeriodForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class TransSetPeriodForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class CostPeriodForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class CostClassPeriodForm(FlaskForm):
    cost_class = SelectField(
        '경비 분류',
        choices=[('D', '경유'), ('G', '휘발유'), ('E', '전기충전'),
                 ('T', '차량관리'), ('N', '생필품'), ('M', '식대'),
                 ('F', '면세품목'), ('O', '기타')],
        validators=[DataRequired()]
    )
    start_date = DateField('시작 일자', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('마지막 일자', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('검색')


class CompanyPeriodForm(FlaskForm):
    start_date = DateField('시작 일자', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('마지막 일자', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('검색')


class CompanyClassPeriodForm(FlaskForm):
    company_class = SelectField(
        '업체 분류',
        choices=[('R', '매출처'), ('P', '매입처')],
        validators=[DataRequired()]
    )
    start_date = DateField('시작 일자', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('마지막 일자', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('검색')


class BalancePeriodForm(FlaskForm):
    start_date = DateField('시작 일자', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('마지막 일자', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('조회')


class TaxPeriodForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class PaperPeriodForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class ElectPeriodForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('검색')


class DeleteForm(FlaskForm):
    submit = SubmitField('삭제')


class CancelForm(FlaskForm):
    submit = SubmitField('탈퇴')





    """
    위 코드에서 COST_CLASS_CHOICES와 PAYMENT_CHOICES는 중괄호 {} 로 둘러싸여 있어 
    set으로 인식됩니다. 그러나 실제로는 키 - 값 쌍으로 정의된 dictionary여야 합니다.
   
   
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
    """