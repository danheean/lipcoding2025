# 멘토-멘티 매칭 앱 테스트 데이터 가이드

## 📊 테스트 데이터 현황

### 👥 사용자 계정 (총 10명)

#### 🎓 멘토 (3명)
| 이름 | 이메일 | 전문 분야 | 비밀번호 |
|------|--------|-----------|----------|
| **Sarah Kim** | sarah.kim@example.com | React, Node.js, System Design | password123 |
| **David Lee** | david.lee@example.com | Leadership, Product Management, Java | password123 |
| New User 2 | newuser2@example.com | (프로필 미완성) | password123 |

#### 🎯 멘티 (7명)
| 이름 | 이메일 | 관심 분야 | 비밀번호 |
|------|--------|-----------|----------|
| **Alex Park** | alex.park@example.com | React, JavaScript | password123 |
| **Emily Chen** | emily.chen@example.com | Full-stack Development | password123 |
| **Michael Wong** | michael.wong@example.com | Python, System Architecture | password123 |
| **Jessica Liu** | jessica.liu@example.com | Product Management | password123 |
| **Ryan Smith** | ryan.smith@example.com | Team Leadership | password123 |
| **Sofia Garcia** | sofia.garcia@example.com | Microservices, Cloud | password123 |
| New User | newuser@example.com | (프로필 미완성) | password123 |

### 💌 매칭 요청 (7개)

#### ✅ 수락된 요청 (4개)
- **Alex Park** → Sarah Kim: React/JavaScript 멘토링
- **Emily Chen** → Sarah Kim: Full-stack 개발
- **Jessica Liu** → David Lee: 프로덕트 매니지먼트
- **Ryan Smith** → David Lee: 팀 리더십

#### ⏳ 대기 중인 요청 (2개)
- **Michael Wong** → Sarah Kim: 시스템 아키텍처
- **Sofia Garcia** → David Lee: 마이크로서비스

#### ❌ 거절된 요청 (1개)
- **Sofia Garcia** → Sarah Kim: 프론트엔드 아키텍처

### 📅 미팅 일정 (7개)

#### 🔄 예정된 미팅 (5개)
- **6월 30일 05:41**: React 기초 멘토링 (Sarah Kim ↔ Alex Park)
- **7월 1일 01:41**: Node.js 백엔드 개발 (Sarah Kim ↔ Emily Chen)
- **7월 2일 07:41**: 프로덕트 매니지먼트 입문 (David Lee ↔ Jessica Liu)
- **7월 4일 02:41**: 팀 리더십과 기술 매니지먼트 (David Lee ↔ Ryan Smith)
- **7월 6일 06:41**: 시스템 아키텍처 설계 (Sarah Kim ↔ Michael Wong)

#### ✅ 완료된 미팅 (2개)
- **6월 24일**: JavaScript 심화 학습 (Sarah Kim ↔ Alex Park)
- **6월 27일**: 마이크로서비스 아키텍처 (David Lee ↔ Sofia Garcia)

---

## 🧪 테스트 시나리오

### 1. 멘토 계정 테스트 (Sarah Kim 추천)

```
이메일: sarah.kim@example.com
비밀번호: password123
```

**테스트 가능한 기능:**
- 📅 **캘린더**: 5개의 미팅 일정 확인
- 📥 **받은 요청**: 1개 대기 중인 요청 처리
- 👤 **프로필**: 완성된 멘토 프로필 확인
- 📊 **대시보드**: 멘토링 현황 종합 확인

### 2. 멘티 계정 테스트 (Alex Park 추천)

```
이메일: alex.park@example.com
비밀번호: password123
```

**테스트 가능한 기능:**
- 📅 **캘린더**: 2개의 미팅 일정 (완료 1개, 예정 1개)
- 🔍 **멘토 검색**: React, JavaScript 키워드로 검색
- 📤 **내 요청**: 수락된 매칭 요청 확인
- 👤 **프로필**: 멘티 프로필 수정

### 3. 다양한 상태 테스트

#### 💌 매칭 요청 상태
- **Pending**: Michael Wong, Sofia Garcia → 멘토 계정으로 수락/거절 테스트
- **Accepted**: 기존 매칭 관계 확인
- **Rejected**: 거절된 요청 히스토리 확인

#### 📅 미팅 상태
- **Scheduled**: 예정된 미팅 수정/취소 테스트
- **Completed**: 완료된 미팅 히스토리 확인

---

## 🚀 빠른 테스트 가이드

### 1단계: 앱 시작
```bash
./start.sh
```

### 2단계: 브라우저 접속
```
http://localhost:3000
```

### 3단계: 계정 로그인
- **멘토 체험**: sarah.kim@example.com / password123
- **멘티 체험**: alex.park@example.com / password123

### 4단계: 기능 테스트
1. **캘린더 확인**: 메인 페이지 상단의 캘린더에서 미팅 일정 확인
2. **프로필 수정**: 이름, 소개, 기술스택 수정
3. **멘토 검색**: (멘티 계정) 기술스택으로 멘토 필터링
4. **요청 관리**: (멘토 계정) 받은 요청 수락/거절
5. **미팅 관리**: 캘린더에서 미팅 추가/수정

---

## 🔧 데이터 초기화

### 사용자 데이터 재생성
```bash
cd backend
python3 create_test_data.py
```

### 미팅 데이터 재생성
```bash
cd backend
python3 create_test_meetings.py
```

### 매칭 요청 데이터 재생성
```bash
cd backend
python3 create_test_requests.py
```

### 전체 데이터 한번에 재생성
```bash
cd backend
python3 create_test_data.py
python3 create_test_meetings.py  
python3 create_test_requests.py
```

---

## 📱 API 테스트

### Swagger UI 접속
```
http://localhost:8080/docs
```

### 주요 API 엔드포인트
- `POST /api/login`: 로그인
- `GET /api/meetings`: 미팅 목록 조회
- `GET /api/meetings/calendar/{year}/{month}`: 캘린더 데이터
- `GET /api/match-requests/incoming`: 받은 요청 목록
- `GET /api/match-requests/outgoing`: 보낸 요청 목록

이제 모든 기능을 완전히 테스트할 수 있는 풍부한 데이터가 준비되었습니다! 🎉
