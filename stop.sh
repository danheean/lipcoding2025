#!/bin/bash

# 스크립트가 있는 디렉토리로 이동 (GitHub Actions 대응)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 멘토-멘티 매칭 앱 전체 시스템 종료"
echo "===================================="
echo "현재 작업 디렉토리: $(pwd)"
echo ""

# 실행 중인 프로세스 확인
echo "🔍 현재 실행 중인 프로세스 확인..."
BACKEND_PROCESSES=$(ps aux | grep -E "(python main.py|uvicorn main:app)" | grep -v grep | wc -l)
FRONTEND_PROCESSES=$(ps aux | grep -E "(npm run dev|vite)" | grep -v grep | wc -l)

echo "   백엔드 프로세스: $BACKEND_PROCESSES개"
echo "   프론트엔드 프로세스: $FRONTEND_PROCESSES개"
echo ""

# 백엔드 종료
if [ "$BACKEND_PROCESSES" -gt 0 ]; then
    echo "🔧 백엔드 서버 종료 중..."
    pkill -f "python main.py" 2>/dev/null
    pkill -f "uvicorn main:app" 2>/dev/null
    echo "   ✅ 백엔드 서버 종료 완료"
else
    echo "ℹ️ 실행 중인 백엔드 서버가 없습니다."
fi

# 프론트엔드 종료
if [ "$FRONTEND_PROCESSES" -gt 0 ]; then
    echo "🎨 프론트엔드 서버 종료 중..."
    pkill -f "npm run dev" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    echo "   ✅ 프론트엔드 서버 종료 완료"
else
    echo "ℹ️ 실행 중인 프론트엔드 서버가 없습니다."
fi

# 종료 대기
sleep 2

# 최종 확인
echo ""
echo "🔍 종료 후 프로세스 확인..."
REMAINING_BACKEND=$(ps aux | grep -E "(python main.py|uvicorn main:app)" | grep -v grep | wc -l)
REMAINING_FRONTEND=$(ps aux | grep -E "(npm run dev|vite)" | grep -v grep | wc -l)

if [ "$REMAINING_BACKEND" -eq 0 ] && [ "$REMAINING_FRONTEND" -eq 0 ]; then
    echo "✅ 모든 서버가 성공적으로 종료되었습니다!"
else
    echo "⚠️ 일부 프로세스가 아직 실행 중일 수 있습니다:"
    if [ "$REMAINING_BACKEND" -gt 0 ]; then
        echo "   백엔드: $REMAINING_BACKEND개 프로세스"
    fi
    if [ "$REMAINING_FRONTEND" -gt 0 ]; then
        echo "   프론트엔드: $REMAINING_FRONTEND개 프로세스"
    fi
    echo ""
    echo "🔧 강제 종료가 필요한 경우:"
    echo "   sudo pkill -9 -f 'python main.py'"
    echo "   sudo pkill -9 -f 'npm run dev'"
fi

echo ""
echo "🎯 시스템 종료 완료!"
echo "=================="
echo "🚀 다시 시작하려면: ./start.sh"
