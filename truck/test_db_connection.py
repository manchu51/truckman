from truck import create_app, db

app = create_app()  # Flask 애플리케이션 생성 및 초기화

with app.app_context():
    # 데이터베이스 또는 SMTP 작업을 여기서 실행합니다.
    # 예: print(db.engine) 로 DB 연결 확인 가능
    print("Database connected successfully.")





"""
from truck import db  # Flask 앱에서 SQLAlchemy 인스턴스 가져오기
from flask import Flask

# 앱 생성 (프로덕션 환경 설정을 사용하도록 보장)
app = Flask(__name__)
app.config.from_object('config.development.DevelopmentConfig')
#app.config.from_object('config.development')  # 'config.production'을 실제 환경에 맞게 조정

# 데이터베이스 연결 테스트
with app.app_context():  # Flask 애플리케이션 컨텍스트 내에서 실행
    try:
        # SQLAlchemy로 데이터베이스 연결 시도
        db.engine.execute('SELECT 1')  # 단순 쿼리 실행
        print("Database connection successful!")  # 연결 성공 메시지 출력
    except Exception as e:
        print("Database connection failed:", e)  # 실패 시 예외 메시지 출력
"""