#!/bin/bash

echo "🚀 멘토-멘티 매칭 앱 전체 시스템 백그라운드 시작"
echo "====================================================="
echo ""

# 기존 프로세스 정리
echo "🧹 기존 프로세스 정리 중..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "python main.py" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# 백엔드 시작
echo "🔧 백엔드 서버 시작 중..."
cd backend
chmod +x start.sh
./start.sh &
BACKEND_PID=$!
cd ..

echo "⏰ 백엔드 시작 대기 중..."
sleep 5

# 프론트엔드 시작
echo "🎨 프론트엔드 서버 시작 중..."
cd frontend
chmod +x start.sh
./start.sh &
FRONTEND_PID=$!
cd ..

echo "⏰ 프론트엔드 시작 대기 중..."
sleep 8

# 서버 상태 확인
echo ""
echo "📊 서버 상태 확인"
echo "=================="

# 백엔드 상태 확인
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/docs)
if [ "$BACKEND_STATUS" = "200" ]; then
    echo "✅ 백엔드 서버: 정상 동작 (포트 8080)"
    echo "   📖 API 문서: http://localhost:8080/docs"
    echo "   🔗 API URL: http://localhost:8080/api"
else
    echo "⚠️ 백엔드 서버: 상태 확인 중... (포트 8080)"
fi

# 프론트엔드 상태 확인
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "✅ 프론트엔드 서버: 정상 동작 (포트 3000)"
    echo "   🌐 앱 URL: http://localhost:3000"
else
    echo "⚠️ 프론트엔드 서버: 상태 확인 중... (포트 3000)"
fi

echo ""
echo "🎯 시스템 시작 완료!"
echo "===================="
echo "📱 앱 접속: http://localhost:3000"
echo "📖 API 문서: http://localhost:8080/docs"
echo ""
echo "🛑 전체 시스템 종료 방법:"
echo "   ./stop.sh"
echo "   또는"
echo "   pkill -f 'python main.py'"
echo "   pkill -f 'npm run dev'"
echo ""
echo "📋 개별 서버 종료:"
echo "   백엔드: pkill -f 'python main.py'"
echo "   프론트엔드: pkill -f 'npm run dev'"
echo ""
echo "🔍 프로세스 확인: ps aux | grep -E '(python main.py|npm run dev|vite)'"
