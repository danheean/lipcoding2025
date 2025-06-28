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

## 프로젝트 구조
```
├── backend/           # FastAPI 백엔드
│   ├── main.py       # 메인 애플리케이션
│   └── requirements.txt
├── frontend/         # React 프론트엔드
│   ├── src/
│   │   ├── App.jsx   # 메인 컴포넌트
│   │   └── index.css # 스타일
│   └── package.json
└── docs/            # 프로젝트 문서
```
