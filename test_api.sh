#!/bin/bash

# 스크립트가 있는 디렉토리로 이동 (GitHub Actions 대응)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 멘토-멘티 매칭 앱 API 테스트 스크립트
# API 명세서 100% 준수 검증을 위한 테스트 실행

echo "🧪 멘토-멘티 매칭 앱 API 테스트"
echo "==============================="
echo "현재 작업 디렉토리: $(pwd)"
echo "테스트 시작 시간: $(date)"
echo ""

API_BASE="http://localhost:8080/api"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 테스트 결과 카운터
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 로그 함수들
log_test() {
    echo -e "${YELLOW}🧪 TEST: $1${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

log_pass() {
    echo -e "${GREEN}✅ PASS: $1${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
}

log_fail() {
    echo -e "${RED}❌ FAIL: $1${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
}

log_section() {
    echo ""
    echo "================================================================"
    echo -e "${BLUE}📋 $1${NC}"
    echo "================================================================"
}

log_info() {
    echo -e "${BLUE}ℹ️  INFO: $1${NC}"
}

# HTTP 상태 코드 확인 함수
check_status() {
    local expected=$1
    local actual=$2
    local description=$3
    
    if [ "$actual" = "$expected" ]; then
        log_pass "$description (Status: $actual)"
    else
        log_fail "$description (Expected: $expected, Got: $actual)"
    fi
}

# JSON 응답 검증 함수
check_json_field() {
    local json=$1
    local field=$2
    local expected=$3
    local description=$4
    
    local actual=$(echo "$json" | jq -r ".$field")
    if [ "$actual" = "$expected" ]; then
        log_pass "$description"
    else
        log_fail "$description (Expected: $expected, Got: $actual)"
    fi
}

# JSON 응답 확인 함수
check_json_field() {
    local response=$1
    local field=$2
    local expected=$3
    local description=$4
    
    local actual=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('$field', 'NOT_FOUND'))")
    
    if [ "$actual" = "$expected" ]; then
        log_pass "$description ($field: $actual)"
    else
        log_fail "$description (Expected $field: $expected, Got: $actual)"
    fi
}

# 테스트 시작
echo "🚀 멘토-멘티 매칭 앱 API 테스트 시작"
echo "📅 $(date)"
echo "🌐 API Base URL: $API_BASE"

# 서버 연결 확인
log_section "서버 연결 확인"
log_test "서버 응답 확인"
SERVER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/test")
check_status "200" "$SERVER_STATUS" "백엔드 서버 연결"

# 1. 인증 테스트
log_section "1. 인증 (Authentication) 테스트"

# 1.1 로그인 테스트
log_test "Sarah Kim 멘토 로그인"
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.kim@example.com",
    "password": "password123"
  }')
LOGIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_BASE/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.kim@example.com",
    "password": "password123"
  }')
check_status "200" "$LOGIN_STATUS" "Sarah Kim 로그인"

# JWT 토큰 추출
SARAH_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

if [ -n "$SARAH_TOKEN" ]; then
    log_pass "JWT 토큰 획득 성공"
else
    log_fail "JWT 토큰 획득 실패"
fi

# David Lee 로그인
log_test "David Lee 멘토 로그인"
DAVID_LOGIN=$(curl -s -X POST "$API_BASE/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "david.lee@example.com", 
    "password": "password123"
  }')
DAVID_TOKEN=$(echo "$DAVID_LOGIN" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

# Alex Park 멘티 로그인  
log_test "Alex Park 멘티 로그인"
ALEX_LOGIN=$(curl -s -X POST "$API_BASE/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alex.park@example.com",
    "password": "password123" 
  }')
ALEX_TOKEN=$(echo "$ALEX_LOGIN" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

# 잘못된 로그인 테스트
log_test "잘못된 비밀번호 로그인 (401 예상)"
WRONG_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_BASE/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.kim@example.com",
    "password": "wrongpassword"
  }')
check_status "401" "$WRONG_STATUS" "잘못된 비밀번호 로그인 거부"

# 2. 사용자 정보 테스트
log_section "2. 사용자 정보 테스트"

# /me 엔드포인트 테스트 (명세서 호환)
log_test "Sarah Kim /me 엔드포인트 조회"
ME_RESPONSE=$(curl -s -X GET "$API_BASE/me" \
  -H "Authorization: Bearer $SARAH_TOKEN")
ME_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/me" \
  -H "Authorization: Bearer $SARAH_TOKEN")
check_status "200" "$ME_STATUS" "/me 엔드포인트 조회"

# 응답 구조 확인
if [ "$ME_STATUS" = "200" ]; then
    check_json_field "$ME_RESPONSE" "role" "mentor" "Sarah Kim 역할 확인"
    check_json_field "$ME_RESPONSE" "email" "sarah.kim@example.com" "Sarah Kim 이메일 확인"
fi

# /profile 엔드포인트 테스트
log_test "Alex Park /profile 엔드포인트 조회"
PROFILE_RESPONSE=$(curl -s -X GET "$API_BASE/profile" \
  -H "Authorization: Bearer $ALEX_TOKEN")
PROFILE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/profile" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "200" "$PROFILE_STATUS" "/profile 엔드포인트 조회"

if [ "$PROFILE_STATUS" = "200" ]; then
    check_json_field "$PROFILE_RESPONSE" "role" "mentee" "Alex Park 역할 확인"
fi

# 인증 실패 테스트
log_test "인증 없이 /me 접근 (401 예상)"
NO_AUTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/me")
check_status "401" "$NO_AUTH_STATUS" "인증 없이 접근 거부"

# 3. 멘토 리스트 테스트
log_section "3. 멘토 리스트 조회 테스트"

# 멘티 권한으로 멘토 리스트 조회
log_test "멘티로 전체 멘토 리스트 조회"
MENTORS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/mentors" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "200" "$MENTORS_STATUS" "멘티의 멘토 리스트 조회"

# 기술스택 필터링 테스트
log_test "JavaScript 기술 필터링"
JS_FILTER_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/mentors?skill=JavaScript" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "200" "$JS_FILTER_STATUS" "JavaScript 스킬 필터링"

# 멘토가 멘토 리스트 접근 시도 (권한 오류 예상)
log_test "멘토로 멘토 리스트 접근 (403 예상)"
MENTOR_ACCESS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/mentors" \
  -H "Authorization: Bearer $SARAH_TOKEN")
check_status "403" "$MENTOR_ACCESS_STATUS" "멘토의 멘토 리스트 접근 거부"

# 4. 매칭 요청 테스트
log_section "4. 매칭 요청 테스트"

# 매칭 요청 생성
log_test "Alex Park이 Sarah Kim에게 매칭 요청"
MATCH_REQUEST=$(curl -s -X POST "$API_BASE/match-requests" \
  -H "Authorization: Bearer $ALEX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mentorId": 1,
    "message": "테스트 매칭 요청입니다!"
  }')
MATCH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_BASE/match-requests" \
  -H "Authorization: Bearer $ALEX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mentorId": 1,
    "message": "테스트 매칭 요청입니다!"
  }')
check_status "200" "$MATCH_STATUS" "매칭 요청 생성"

# 요청 ID 추출
if [ "$MATCH_STATUS" = "200" ]; then
    REQUEST_ID=$(echo "$MATCH_REQUEST" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)
    if [ -n "$REQUEST_ID" ]; then
        log_pass "매칭 요청 ID 획득: $REQUEST_ID"
    fi
fi

# 멘토가 받은 요청 조회
log_test "Sarah Kim이 받은 요청 목록 조회"
INCOMING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/match-requests/incoming" \
  -H "Authorization: Bearer $SARAH_TOKEN")
check_status "200" "$INCOMING_STATUS" "멘토의 받은 요청 조회"

# 멘티가 보낸 요청 조회
log_test "Alex Park이 보낸 요청 목록 조회"
OUTGOING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/match-requests/outgoing" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "200" "$OUTGOING_STATUS" "멘티의 보낸 요청 조회"

# 요청 수락 테스트 (REQUEST_ID가 있을 때만)
if [ -n "$REQUEST_ID" ]; then
    log_test "Sarah Kim이 요청 수락"
    ACCEPT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$API_BASE/match-requests/$REQUEST_ID/accept" \
      -H "Authorization: Bearer $SARAH_TOKEN")
    check_status "200" "$ACCEPT_STATUS" "매칭 요청 수락"
fi

# 5. 이미지 엔드포인트 테스트
log_section "5. 이미지 엔드포인트 테스트"

log_test "멘토 프로필 이미지 조회 (인증 필요)"
IMAGE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/images/mentor/1" \
  -H "Authorization: Bearer $SARAH_TOKEN")
# 이미지가 없으면 기본 이미지로 리다이렉트되므로 200 또는 302 둘 다 정상
if [ "$IMAGE_STATUS" = "200" ] || [ "$IMAGE_STATUS" = "302" ]; then
    log_pass "멘토 이미지 조회 (Status: $IMAGE_STATUS)"
else
    log_fail "멘토 이미지 조회 (Expected: 200 or 302, Got: $IMAGE_STATUS)"
fi

log_test "이미지 조회 시 인증 없이 접근 (401 예상)"
NO_AUTH_IMAGE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/images/mentor/1")
check_status "401" "$NO_AUTH_IMAGE_STATUS" "인증 없는 이미지 조회"

# 6. API 명세서 준수 검증 테스트
log_section "6. API 명세서 100% 준수 검증"

# 6.1 회원가입 에러 검증
log_test "잘못된 role로 회원가입 (400 예상)"
INVALID_ROLE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_BASE/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid@example.com",
    "password": "password123",
    "name": "Invalid User",
    "role": "invalid_role"
  }')
check_status "400" "$INVALID_ROLE_STATUS" "잘못된 role 회원가입"

# 6.2 /me 엔드포인트 응답 형식 검증
log_test "/me 엔드포인트 응답 형식 검증"
ME_RESPONSE=$(curl -s -X GET "$API_BASE/me" \
  -H "Authorization: Bearer $SARAH_TOKEN")
ME_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/me" \
  -H "Authorization: Bearer $SARAH_TOKEN")
check_status "200" "$ME_STATUS" "/me 엔드포인트 응답"

# 멘토 응답에 필수 필드 확인
if [ "$ME_STATUS" = "200" ]; then
    check_json_field "$ME_RESPONSE" "id" "1" "멘토 ID 필드"
    check_json_field "$ME_RESPONSE" "email" "sarah.kim@example.com" "멘토 이메일 필드"
    check_json_field "$ME_RESPONSE" "role" "mentor" "멘토 role 필드"
    
    # profile 내부 필드 확인
    PROFILE_NAME=$(echo "$ME_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('profile', {}).get('name', 'NOT_FOUND'))" 2>/dev/null)
    PROFILE_BIO=$(echo "$ME_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('profile', {}).get('bio', 'NOT_FOUND'))" 2>/dev/null)
    PROFILE_IMAGE=$(echo "$ME_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('profile', {}).get('imageUrl', 'NOT_FOUND'))" 2>/dev/null)
    
    if [ "$PROFILE_NAME" != "NOT_FOUND" ]; then
        log_pass "멘토 profile.name 필드 존재"
    else
        log_fail "멘토 profile.name 필드 누락"
    fi
    
    if [ "$PROFILE_IMAGE" = "/api/images/mentor/1" ]; then
        log_pass "멘토 profile.imageUrl 형식"
    else
        log_fail "멘토 profile.imageUrl 형식 (Expected: /api/images/mentor/1, Got: $PROFILE_IMAGE)"
    fi
fi

# 6.3 멘토 리스트 응답 형식 검증
log_test "멘토 리스트 응답 형식 검증"
MENTORS_RESPONSE=$(curl -s -X GET "$API_BASE/mentors" \
  -H "Authorization: Bearer $ALEX_TOKEN")
MENTORS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/mentors" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "200" "$MENTORS_STATUS" "멘토 리스트 조회"

if [ "$MENTORS_STATUS" = "200" ]; then
    # 배열인지 확인
    IS_ARRAY=$(echo "$MENTORS_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(isinstance(data, list))" 2>/dev/null)
    if [ "$IS_ARRAY" = "True" ]; then
        log_pass "멘토 리스트가 배열 형식"
    else
        log_fail "멘토 리스트가 배열 형식이 아님"
    fi
    
    # 첫 번째 멘토의 필드 확인
    FIRST_MENTOR_EMAIL=$(echo "$MENTORS_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[0].get('email', 'NOT_FOUND') if len(data) > 0 else 'NOT_FOUND')" 2>/dev/null)
    if [ "$FIRST_MENTOR_EMAIL" != "NOT_FOUND" ]; then
        log_pass "멘토 리스트 첫 번째 멘토에 email 필드 존재"
    else
        log_fail "멘토 리스트 첫 번째 멘토에 email 필드 누락"
    fi
fi

# 6.4 매칭 요청 outgoing 응답 형식 검증 (message 필드 누락 확인)
log_test "매칭 요청 outgoing 응답 형식 검증"
OUTGOING_RESPONSE=$(curl -s -X GET "$API_BASE/match-requests/outgoing" \
  -H "Authorization: Bearer $ALEX_TOKEN")
OUTGOING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/match-requests/outgoing" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "200" "$OUTGOING_STATUS" "outgoing 매칭 요청 목록"

if [ "$OUTGOING_STATUS" = "200" ]; then
    # 배열인지 확인
    IS_ARRAY=$(echo "$OUTGOING_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(isinstance(data, list))" 2>/dev/null)
    if [ "$IS_ARRAY" = "True" ]; then
        log_pass "outgoing 매칭 요청이 배열 형식"
    else
        log_fail "outgoing 매칭 요청이 배열 형식이 아님"
    fi
    
    # message 필드가 없어야 함 (명세서에 따라)
    if echo "$OUTGOING_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(any('message' in item for item in data) if len(data) > 0 else False)" 2>/dev/null | grep -q "False"; then
        log_pass "outgoing 요청에 message 필드 누락 (명세서 준수)"
    else
        log_fail "outgoing 요청에 message 필드가 있음 (명세서 위반)"
    fi
fi

# 6.5 에러 응답 형식 검증
log_test "존재하지 않는 매칭 요청 수락 시도 (404 예상)"
INVALID_ACCEPT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$API_BASE/match-requests/99999/accept" \
  -H "Authorization: Bearer $SARAH_TOKEN")
check_status "404" "$INVALID_ACCEPT_STATUS" "존재하지 않는 요청 수락"

log_test "멘티가 매칭 요청 수락 시도 (403 예상)"
MENTEE_ACCEPT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$API_BASE/match-requests/1/accept" \
  -H "Authorization: Bearer $ALEX_TOKEN")
check_status "403" "$MENTEE_ACCEPT_STATUS" "멘티의 요청 수락 시도"

log_test "멘토가 outgoing 요청 조회 시도 (403 예상)"  
MENTOR_OUTGOING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$API_BASE/match-requests/outgoing" \
  -H "Authorization: Bearer $SARAH_TOKEN")
check_status "403" "$MENTOR_OUTGOING_STATUS" "멘토의 outgoing 요청 조회"

# 테스트 결과 요약
log_section "테스트 결과 요약"
echo "📊 총 테스트: $TOTAL_TESTS"
echo "✅ 성공: $PASSED_TESTS"
echo "❌ 실패: $FAILED_TESTS"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 모든 테스트 통과!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  $FAILED_TESTS개 테스트 실패${NC}"
    exit 1
fi
