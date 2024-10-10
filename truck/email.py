import os

from flask_mail import Message
from truck import mail
from itsdangerous import URLSafeTimedSerializer as Serializer
#from itsdangerous import URLSafeTimedSerializer
from flask import url_for
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

def get_reset_token(user, expires_sec=1800):
    # Ensure the SECRET_KEY is a byte string
    secret_key = current_app.config['SECRET_KEY']

    # Convert the secret_key to bytes if it's not
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    #s = Serializer(secret_key, expires_sec, salt=b'my-salt')
    s = Serializer(secret_key, expires_sec)

    return s.dumps({'user_id': user.id})

    #s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #return s.dumps({'user_id': user.id})    # Removed .decode('utf-8')



def send_reset_email(user, token):
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg = Message(
        '비밀번호 재설정 요청',
        sender=os.getenv('MAIL_DEFAULT_SENDER'),  # 기본 발신자 정보를 .env에서 가져옴
        recipients=[user.email]
    )

    msg.body = f'''비밀번호를 재설정하려면 아래 링크를 클릭하세요:
    {reset_url}

    만약 본인이 요청하지 않았다면, 이 이메일을 무시하셔도 됩니다. 
    '''

    mail.send(msg)


