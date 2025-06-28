#!/bin/bash

echo "=== 멘토-멘티 매칭 앱 백엔드 시작 ==="
echo "포트: 8080"
echo "Swagger UI: http://localhost:8080/docs"
echo ""

# 가상 환경이 있다면 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 의존성 설치
echo "의존성 설치 중..."
pip install -r requirements.txt

# 애플리케이션 시작
echo "FastAPI 서버 시작 중..."
python main.py
