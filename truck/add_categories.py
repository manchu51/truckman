import os
import sys

# 현재 경로에 truck 디렉터리가 추가되도록 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from truck import create_app, db  # 'truck' 모듈에서 create_app과 db 가져오기
from truck.models import Category  # Category 모델 가져오기

# Flask 앱 생성
app = create_app()

# Flask 앱 컨텍스트에서 카테고리를 추가하는 작업
with app.app_context():
    # 새로운 카테고리 목록
    categories = ['화물세상', '질문과답변', '자유게시판', '버그및건의']

    for name in categories:
        # 카테고리 객체 생성 및 DB 세션에 추가
        category = Category(name=name)
        db.session.add(category)

    # DB에 변경 사항 커밋
    db.session.commit()

    print("카테고리가 성공적으로 추가되었습니다.")




