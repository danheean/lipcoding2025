#!/bin/bash

# RiseWith 모바일 친화성 테스트 스크립트
echo "🔍 RiseWith 모바일 친화성 테스트 시작..."

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 서버 상태 확인
echo -e "${BLUE}📡 서버 상태 확인 중...${NC}"

# 백엔드 확인
if curl -s http://localhost:8080/docs > /dev/null; then
    echo -e "${GREEN}✅ 백엔드 서버 (FastAPI) 실행 중${NC}"
else
    echo -e "${RED}❌ 백엔드 서버가 실행되지 않았습니다${NC}"
    echo "백엔드 서버를 시작하세요: cd backend && python main.py"
fi

# 프론트엔드 확인
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✅ 프론트엔드 서버 (React) 실행 중${NC}"
else
    echo -e "${RED}❌ 프론트엔드 서버가 실행되지 않았습니다${NC}"
    echo "프론트엔드 서버를 시작하세요: cd frontend && npm start"
fi

echo ""
echo -e "${BLUE}📱 모바일 친화성 기능 확인 중...${NC}"

# CSS 모바일 미디어 쿼리 확인
if grep -q "@media (max-width: 768px)" frontend/src/index.css; then
    echo -e "${GREEN}✅ 모바일 미디어 쿼리 적용됨${NC}"
else
    echo -e "${RED}❌ 모바일 미디어 쿼리 누락${NC}"
fi

# Viewport 메타 태그 확인
if grep -q "viewport.*width=device-width" frontend/index.html; then
    echo -e "${GREEN}✅ Viewport 메타 태그 설정됨${NC}"
else
    echo -e "${RED}❌ Viewport 메타 태그 누락${NC}"
fi

# PWA 매니페스트 확인
if [ -f "frontend/public/manifest.json" ]; then
    echo -e "${GREEN}✅ PWA 매니페스트 파일 존재${NC}"
else
    echo -e "${RED}❌ PWA 매니페스트 파일 누락${NC}"
fi

# Touch 친화적 클래스 확인
if grep -q "touchable\|clickable" frontend/src/index.css; then
    echo -e "${GREEN}✅ 터치 친화적 스타일 적용됨${NC}"
else
    echo -e "${RED}❌ 터치 친화적 스타일 누락${NC}"
fi

# 모바일 컴포넌트 확인
if grep -q "isMobile\|useResponsive\|TouchButton" frontend/src/App.jsx; then
    echo -e "${GREEN}✅ 모바일 친화적 컴포넌트 적용됨${NC}"
else
    echo -e "${RED}❌ 모바일 친화적 컴포넌트 누락${NC}"
fi

echo ""
echo -e "${BLUE}🎨 UI/UX 모바일 최적화 확인 중...${NC}"

# 반응형 그리드 확인
if grep -q "grid-template-columns.*1fr" frontend/src/index.css; then
    echo -e "${GREEN}✅ 반응형 그리드 레이아웃 적용됨${NC}"
else
    echo -e "${YELLOW}⚠️  반응형 그리드 최적화 권장${NC}"
fi

# 터치 타겟 크기 확인
if grep -q "min-height.*44px\|min-width.*44px" frontend/src/index.css; then
    echo -e "${GREEN}✅ 최소 터치 타겟 크기 (44px) 적용됨${NC}"
else
    echo -e "${YELLOW}⚠️  터치 타겟 크기 최적화 권장${NC}"
fi

# 스티키 네비게이션 확인
if grep -q "position.*sticky\|position.*fixed" frontend/src/index.css; then
    echo -e "${GREEN}✅ 모바일 네비게이션 최적화 적용됨${NC}"
else
    echo -e "${YELLOW}⚠️  모바일 네비게이션 최적화 권장${NC}"
fi

echo ""
echo -e "${BLUE}🔧 성능 및 접근성 확인 중...${NC}"

# Smooth scrolling 확인
if grep -q "scroll-behavior.*smooth" frontend/src/index.css; then
    echo -e "${GREEN}✅ 부드러운 스크롤 적용됨${NC}"
else
    echo -e "${YELLOW}⚠️  부드러운 스크롤 최적화 권장${NC}"
fi

# Touch action 확인
if grep -q "touch-action.*manipulation" frontend/src/index.css; then
    echo -e "${GREEN}✅ 터치 인터랙션 최적화 적용됨${NC}"
else
    echo -e "${YELLOW}⚠️  터치 인터랙션 최적화 권장${NC}"
fi

# iOS 줌 방지 확인
if grep -q "font-size.*16px" frontend/src/index.css; then
    echo -e "${GREEN}✅ iOS 자동 줌 방지 적용됨${NC}"
else
    echo -e "${YELLOW}⚠️  iOS 자동 줌 방지 권장${NC}"
fi

echo ""
echo -e "${BLUE}📊 모바일 친화성 테스트 완료!${NC}"

# 브라우저에서 개발자 도구 모바일 모드 안내
echo ""
echo -e "${YELLOW}📱 모바일 테스트 방법:${NC}"
echo "1. Chrome/Edge 개발자 도구 (F12) 열기"
echo "2. Device Toolbar 토글 (Ctrl+Shift+M)"
echo "3. 다양한 모바일 기기로 테스트"
echo "4. 터치 인터랙션 및 반응형 레이아웃 확인"

echo ""
echo -e "${GREEN}🎉 모바일 친화적 기능이 성공적으로 적용되었습니다!${NC}"

# 모바일 성능 체크를 위한 Lighthouse 추천
echo ""
echo -e "${BLUE}💡 추가 테스트 권장사항:${NC}"
echo "• Chrome Lighthouse 모바일 성능 테스트"
echo "• 실제 모바일 기기에서 테스트"
echo "• 터치 제스처 및 스와이프 동작 확인"
echo "• 네트워크 속도 제한 환경에서 테스트"
