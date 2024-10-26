from flask_mail import Message
from truck import mail  # mail 객체를 정의한 위치에서 가져옴
from flask import url_for, current_app
import os
from itsdangerous import URLSafeTimedSerializer

def get_reset_token(user_id):
    """비밀번호 재설정 토큰 생성"""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user_id})

def send_reset_email(user, token):
    """비밀번호 재설정 이메일 전송"""
    msg = Message(
        '비밀번호 재설정 요청',
        sender=os.getenv('MAIL_DEFAULT_SENDER'),
        recipients=[user.email]
    )
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg.body = f'''
    비밀번호 재설정을 요청하셨습니다. 아래 링크를 클릭하여 비밀번호를 재설정하세요:
    {reset_url}

    만약 본인이 요청하지 않았다면 이 이메일을 무시하세요.
    '''
    mail.send(msg)

