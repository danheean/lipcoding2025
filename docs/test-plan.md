# 멘토-멘티 매칭 앱 테스트 계획서

## 📋 테스트 개요

### 테스트 목표
- API 명세서에 정의된 모든 엔드포인트의 정상 작동 확인
- 프론트엔드와 백엔드 간 통합 테스트
- 사용자 시나리오 기반 E2E 테스트
- 에러 처리 및 예외 상황 테스트

### 테스트 환경
- **백엔드**: http://localhost:8080
- **프론트엔드**: http://localhost:3001
- **데이터베이스**: SQLite (mentor_mentee.db)
- **테스트 계정**: 멘토 2명, 멘티 6명

---

## 🔐 1. 인증 (Authentication) 테스트

### 1.1 회원가입 테스트 (POST `/signup`)

#### 정상 케이스
- [ ] 멘토 회원가입 성공 (201 Created)
- [ ] 멘티 회원가입 성공 (201 Created)

#### 에러 케이스
- [ ] 이메일 중복 (400 Bad Request)
- [ ] 잘못된 이메일 형식 (400 Bad Request)
- [ ] 필수 필드 누락 (400 Bad Request)
- [ ] 잘못된 role 값 (400 Bad Request)

**테스트 데이터:**
```json
// 정상 케이스
{
  "email": "test.mentor@example.com",
  "password": "testpass123",
  "name": "테스트 멘토",
  "role": "mentor"
}

// 에러 케이스
{
  "email": "invalid-email",
  "password": "",
  "name": "",
  "role": "invalid"
}
```

### 1.2 로그인 테스트 (POST `/login`)

#### 정상 케이스
- [ ] 멘토 로그인 성공 (JWT 토큰 반환)
- [ ] 멘티 로그인 성공 (JWT 토큰 반환)
- [ ] 기존 테스트 계정들 로그인 확인

#### 에러 케이스
- [ ] 잘못된 이메일 (401 Unauthorized)
- [ ] 잘못된 비밀번호 (401 Unauthorized)
- [ ] 존재하지 않는 계정 (401 Unauthorized)
- [ ] 빈 요청 body (400 Bad Request)

**테스트 계정:**
- Sarah Kim: sarah.kim@example.com / password123
- David Lee: david.lee@example.com / password123
- Alex Park: alex.park@example.com / password123

---

## 👤 2. 사용자 정보 테스트

### 2.1 내 정보 조회 테스트 (GET `/me` → `/profile`)

#### 정상 케이스
- [ ] 멘토 프로필 조회 (skills 포함)
- [ ] 멘티 프로필 조회 (skills 제외)
- [ ] 응답 데이터 구조 검증

#### 에러 케이스
- [ ] 토큰 없음 (401 Unauthorized)
- [ ] 잘못된 토큰 (401 Unauthorized)
- [ ] 만료된 토큰 (401 Unauthorized)

### 2.2 프로필 이미지 테스트 (GET `/images/:role/:id`)

#### 정상 케이스
- [ ] 멘토 이미지 조회/기본 이미지 반환
- [ ] 멘티 이미지 조회/기본 이미지 반환

#### 에러 케이스
- [ ] 인증 실패 (401 Unauthorized)
- [ ] 존재하지 않는 사용자 ID

### 2.3 프로필 수정 테스트 (PUT `/profile`)

#### 정상 케이스
- [ ] 멘토 프로필 수정 (이름, 소개, 기술스택)
- [ ] 멘티 프로필 수정 (이름, 소개)
- [ ] 이미지 업로드 (Base64)
- [ ] 부분 업데이트 (일부 필드만 수정)

#### 에러 케이스
- [ ] 인증 실패 (401 Unauthorized)
- [ ] 잘못된 이미지 형식 (400 Bad Request)
- [ ] 필수 필드 누락 (400 Bad Request)

**테스트 데이터:**
```json
// 멘토 프로필 수정
{
  "id": 1,
  "name": "Updated Sarah Kim",
  "role": "mentor",
  "bio": "Updated bio for testing",
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "skills": ["React", "Node.js", "Testing"]
}
```

---

## 👥 3. 멘토 리스트 조회 테스트

### 3.1 전체 멘토 리스트 (GET `/mentors`)

#### 정상 케이스 (멘티 권한)
- [ ] 전체 멘토 리스트 조회
- [ ] 기술스택 필터링 (`?skill=JavaScript`)
- [ ] 이름순 정렬 (`?order_by=name`)
- [ ] 기술순 정렬 (`?order_by=skill`)
- [ ] 빈 결과 처리 (`?skill=NonExistentSkill`)

#### 에러 케이스
- [ ] 멘토가 접근 시 (403 Forbidden)
- [ ] 인증 실패 (401 Unauthorized)

**테스트 쿼리:**
- `/mentors` - 전체 조회
- `/mentors?skill=JavaScript` - JavaScript 스킬 필터
- `/mentors?skill=Leadership` - Leadership 스킬 필터
- `/mentors?order_by=name` - 이름순 정렬
- `/mentors?order_by=skill` - 기술순 정렬

---

## 🤝 4. 멘토 매칭 요청 테스트

### 4.1 매칭 요청 보내기 (POST `/match-requests`)

#### 정상 케이스 (멘티 권한)
- [ ] 멘토에게 매칭 요청 전송
- [ ] 응답 데이터 구조 확인 (id, status="pending")
- [ ] 다른 멘토에게 추가 요청

#### 에러 케이스
- [ ] 멘토가 접근 시 (403 Forbidden)
- [ ] 존재하지 않는 멘토 ID (400 Bad Request)
- [ ] 잘못된 요청 body (400 Bad Request)
- [ ] 인증 실패 (401 Unauthorized)

**테스트 데이터:**
```json
{
  "mentorId": 1,
  "menteeId": 3,
  "message": "React와 JavaScript를 배우고 싶습니다!"
}
```

### 4.2 받은 요청 목록 (GET `/match-requests/incoming`)

#### 정상 케이스 (멘토 권한)
- [ ] 멘토가 받은 요청 목록 조회
- [ ] 다양한 상태 요청 확인 (pending, accepted, rejected, cancelled)
- [ ] 빈 목록 처리

#### 에러 케이스
- [ ] 멘티가 접근 시 (403 Forbidden)
- [ ] 인증 실패 (401 Unauthorized)

### 4.3 보낸 요청 목록 (GET `/match-requests/outgoing`)

#### 정상 케이스 (멘티 권한)
- [ ] 멘티가 보낸 요청 목록 조회
- [ ] 요청 상태별 확인
- [ ] 빈 목록 처리

#### 에러 케이스
- [ ] 멘토가 접근 시 (403 Forbidden)
- [ ] 인증 실패 (401 Unauthorized)

### 4.4 요청 수락 (PUT `/match-requests/:id/accept`)

#### 정상 케이스 (멘토 권한)
- [ ] pending 요청 수락
- [ ] status가 "accepted"로 변경 확인
- [ ] 수락 후 요청 목록에서 상태 변경 확인

#### 에러 케이스
- [ ] 멘티가 접근 시 (403 Forbidden)
- [ ] 존재하지 않는 요청 ID (404 Not Found)
- [ ] 이미 처리된 요청 수락 시도
- [ ] 인증 실패 (401 Unauthorized)

### 4.5 요청 거절 (PUT `/match-requests/:id/reject`)

#### 정상 케이스 (멘토 권한)
- [ ] pending 요청 거절
- [ ] status가 "rejected"로 변경 확인

#### 에러 케이스
- [ ] 멘티가 접근 시 (403 Forbidden)
- [ ] 존재하지 않는 요청 ID (404 Not Found)
- [ ] 인증 실패 (401 Unauthorized)

### 4.6 요청 취소/삭제 (DELETE `/match-requests/:id`)

#### 정상 케이스 (멘티 권한)
- [ ] 자신이 보낸 요청 취소
- [ ] status가 "cancelled"로 변경 확인

#### 에러 케이스
- [ ] 멘토가 접근 시 (403 Forbidden)
- [ ] 존재하지 않는 요청 ID (404 Not Found)
- [ ] 다른 멘티의 요청 취소 시도
- [ ] 인증 실패 (401 Unauthorized)

---

## 🌐 5. 프론트엔드 통합 테스트

### 5.1 사용자 인터페이스 테스트

#### 로그인 페이지
- [ ] 수동 로그인 폼 작동
- [ ] 빠른 로그인 버튼들 작동
- [ ] 에러 메시지 표시
- [ ] 로그인 성공 시 프로필 페이지 이동

#### 프로필 페이지
- [ ] 사용자 정보 표시
- [ ] 프로필 수정 기능
- [ ] 이미지 업로드 기능
- [ ] 멘토/멘티별 UI 차이 확인

#### 멘토 리스트 페이지 (멘티만)
- [ ] 멘토 목록 표시
- [ ] 기술스택 필터링
- [ ] 정렬 기능
- [ ] "Request Mentorship" 버튼

#### 매칭 요청 페이지
- [ ] 받은 요청 목록 (멘토)
- [ ] 보낸 요청 목록 (멘티)
- [ ] 수락/거절 버튼 (멘토)
- [ ] 취소 버튼 (멘티)

### 5.2 테스트 ID 확인
- [ ] `id="email"` - 이메일 입력 필드
- [ ] `id="password"` - 비밀번호 입력 필드
- [ ] `id="login"` - 로그인 버튼

---

## 🔄 6. E2E 사용자 시나리오 테스트

### 시나리오 1: 새로운 멘티의 멘토 찾기
1. [ ] 멘티 회원가입
2. [ ] 로그인
3. [ ] 멘토 리스트 조회
4. [ ] 기술스택으로 필터링
5. [ ] 원하는 멘토에게 매칭 요청
6. [ ] 요청 상태 확인

### 시나리오 2: 멘토의 요청 관리
1. [ ] 멘토 로그인
2. [ ] 받은 요청 목록 확인
3. [ ] 요청 수락/거절
4. [ ] 상태 변경 확인

### 시나리오 3: 프로필 관리
1. [ ] 사용자 로그인
2. [ ] 프로필 정보 수정
3. [ ] 이미지 업로드
4. [ ] 변경사항 저장 및 확인

---

## 🛠️ 7. 기술적 테스트

### 7.1 API 응답 형식 검증
- [ ] Content-Type: application/json
- [ ] 응답 스키마 일치성 확인
- [ ] 상태 코드 정확성

### 7.2 보안 테스트
- [ ] JWT 토큰 검증
- [ ] CORS 설정 확인
- [ ] SQL Injection 방지
- [ ] XSS 방지

### 7.3 성능 테스트
- [ ] API 응답 시간 측정
- [ ] 다중 사용자 동시 접근
- [ ] 이미지 업로드 처리 시간

---

## 📊 8. 테스트 자동화 계획

### 8.1 API 테스트 자동화
```bash
# curl 기반 스크립트
./test_api.sh

# 또는 Postman Collection
npm run test:api
```

### 8.2 프론트엔드 테스트
```bash
# E2E 테스트 (예: Playwright)
npm run test:e2e

# 단위 테스트
npm run test:unit
```

---

## ✅ 9. 테스트 체크리스트

### 사전 준비
- [ ] 백엔드 서버 실행 (포트 8080)
- [ ] 프론트엔드 서버 실행 (포트 3001)
- [ ] 테스트 데이터 생성 확인
- [ ] 데이터베이스 초기 상태 확인

### 테스트 실행 순서
1. [ ] 인증 테스트 (회원가입, 로그인)
2. [ ] 사용자 정보 테스트 (프로필 조회/수정)
3. [ ] 멘토 리스트 테스트 (조회, 필터링)
4. [ ] 매칭 요청 테스트 (생성, 조회, 상태 변경)
5. [ ] 프론트엔드 통합 테스트
6. [ ] E2E 시나리오 테스트

### 테스트 결과 문서화
- [ ] 각 테스트 케이스별 통과/실패 기록
- [ ] 발견된 버그 및 개선사항 정리
- [ ] 성능 측정 결과 기록
- [ ] 사용자 경험 피드백 수집

---

## 🎯 10. 예상 테스트 결과

### 현재 구현 상태 기준 예상 결과
- ✅ **인증**: 로그인/회원가입 정상 작동
- ✅ **프로필**: 조회/수정 기능 정상
- ✅ **멘토 리스트**: 조회/필터링 정상
- ✅ **매칭 요청**: 생성/조회/상태변경 정상
- ⚠️ **프론트엔드**: 일부 UI 개선 필요 가능성
- ⚠️ **에러 처리**: 세부 검증 필요

이 테스트 계획을 바탕으로 체계적인 품질 검증을 수행할 수 있습니다.
