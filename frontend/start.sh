#!/bin/bash

echo "=== 멘토-멘티 매칭 앱 프론트엔드 시작 ==="
echo "포트: 3000"
echo "URL: http://localhost:3000"
echo ""

# 의존성 설치
echo "의존성 설치 중..."
npm install

# 애플리케이션 시작
echo "React 앱 백그라운드로 시작 중..."
echo "서버 종료: pkill -f 'npm start' 또는 pkill -f 'vite'"
npm run dev -- --port 3000 &

# 서버 시작 대기
sleep 5

# 서버 상태 확인
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ React 앱이 성공적으로 시작되었습니다!"
    echo "🌐 앱 URL: http://localhost:3000"
else
    echo "⚠️ 서버 시작을 확인 중입니다..."
    echo "🌐 앱 URL: http://localhost:3000"
fi

echo ""
echo "백그라운드 프로세스 ID: $!"
echo "서버 종료 방법: pkill -f 'npm run dev' 또는 pkill -f 'vite'"
