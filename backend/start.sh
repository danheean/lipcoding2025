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
echo "FastAPI 서버 백그라운드로 시작 중..."
echo "서버 종료: pkill -f 'uvicorn main:app' 또는 pkill -f 'python main.py'"
python main.py &

# 서버 시작 대기
sleep 3

# 서버 상태 확인
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/docs | grep -q "200"; then
    echo "✅ FastAPI 서버가 성공적으로 시작되었습니다!"
    echo "📖 API 문서: http://localhost:8080/docs"
    echo "🔗 API 기본 URL: http://localhost:8080/api"
else
    echo "⚠️ 서버 시작을 확인 중입니다..."
    echo "📖 API 문서: http://localhost:8080/docs"
fi

echo ""
echo "백그라운드 프로세스 ID: $!"
echo "서버 종료 방법: pkill -f 'python main.py'"
