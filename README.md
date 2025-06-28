# 멘토-멘티 매칭 앱

## 개요
멘토와 멘티를 연결하는 매칭 플랫폼입니다. 멘토는 자신의 기술 스택과 소개를 등록하고, 멘티는 원하는 멘토에게 매칭 요청을 보낼 수 있습니다.

## 기술 스택
- **백엔드**: Python FastAPI + SQLite
- **프론트엔드**: React + Vite
- **인증**: JWT 토큰
- **스타일링**: CSS (모던 그라디언트 디자인)

## 실행 방법

### 1. 백엔드 실행 (포트 8080)
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. 프론트엔드 실행 (포트 3000)
```bash
cd frontend
npm install
npm start
```

## 접속 URL
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8080/api
- Swagger UI: http://localhost:8080/docs

## 주요 기능
1. **회원가입/로그인**: 이메일 기반 인증, JWT 토큰
2. **프로필 관리**: 이름, 소개, 프로필 이미지, 기술스택(멘토)
3. **멘토 검색**: 기술스택 필터링, 이름/스킬 정렬
4. **매칭 요청**: 1:1 매칭 시스템
5. **요청 관리**: 수락/거절/취소

## API 문서
- [API 명세서](docs/mentor-mentee-api-spec.md)
- [OpenAPI 스키마](docs/openapi.yaml)
- [사용자 스토리](docs/mentor-mentee-app-user-stories.md)

## 테스트 계정
데이터베이스에 미리 생성된 테스트 계정들을 사용해서 앱을 테스트할 수 있습니다.

**모든 계정의 비밀번호**: `password123`

### 멘토 계정 (2명)
1. **Sarah Kim** (sarah.kim@example.com)
   - 8년차 풀스택 개발자
   - 기술: JavaScript, React, Node.js, Python, System Design, AWS, MongoDB

2. **David Lee** (david.lee@example.com)
   - 10년차 테크리드 & 프로덕트 매니저
   - 기술: Leadership, Product Management, Java, Spring Boot, Microservices, Docker, Kubernetes, PostgreSQL

### 멘티 계정 (6명)

**Sarah Kim의 멘티들:**
- **Alex Park** (alex.park@example.com) - 컴퓨터공학과 학생, 웹개발 학습 중
- **Emily Chen** (emily.chen@example.com) - 부트캠프 졸업생, 풀스택 개발 지도 필요
- **Michael Wong** (michael.wong@example.com) - 1년차 주니어 개발자, 코딩 스킬 향상 원함

**David Lee의 멘티들:**
- **Jessica Liu** (jessica.liu@example.com) - 마케팅에서 테크로 전직, 프로덕트 매니지먼트 관심
- **Ryan Smith** (ryan.smith@example.com) - 테크 리더십 역할 전환 희망하는 개발자
- **Sofia Garcia** (sofia.garcia@example.com) - 마이크로서비스와 클라우드 기술 학습 원하는 미드레벨 개발자

## 프로젝트 구조
```
├── backend/           # FastAPI 백엔드
│   ├── main.py       # 메인 애플리케이션
│   ├── requirements.txt
│   ├── create_test_data.py  # 테스트 데이터 생성 스크립트
│   └── list_users.py       # 사용자 목록 조회 스크립트
├── frontend/         # React 프론트엔드
│   ├── src/
│   │   ├── App.jsx   # 메인 컴포넌트
│   │   └── index.css # 스타일
│   └── package.json
└── docs/            # 프로젝트 문서
```
