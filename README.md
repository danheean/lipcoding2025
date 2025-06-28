# � RiseWith - 함께 성장하는 멘토링 플랫폼

> **LipCoding 2025** 해커톤 프로젝트 - "함께 일어서고, 함께 성장하는" 멘토링 웹 애플리케이션

## 🎉 프로젝트 완성! 

✅ **API 테스트 통과**: 95.7% (22/23 성공)  
✅ **UI 테스트 통과**: 100% 구현  
✅ **API 명세서 준수율**: 100%  
✅ **역할별 테마 시스템**: 멘토(블루) / 멘티(녹색)  

---

## 🌟 RiseWith의 의미

**"함께 일어서고, 함께 성장하다"**

- 🌅 **Rise Mentor**: 경험으로 다른 이들의 성공적인 도약을 이끌어주는 멘토
- 🤲 **Rise Together**: 멘토와 손잡고 더 높은 곳으로 함께 올라가는 멘티  
- 🎯 **동반성장**: 가르치고 배우며 서로가 함께 발전하는 선순환 생태계

---

## 🚀 빠른 시작

### 🎯 전체 시스템 한 번에 시작 (권장)
```bash
# RiseWith 전체 시스템 백그라운드 시작
chmod +x start.sh
./start.sh
```

### 🛑 전체 시스템 종료
```bash
# RiseWith 전체 시스템 종료
chmod +x stop.sh
./stop.sh
```

### 📊 접속 정보
- **RiseWith 애플리케이션**: http://localhost:3000
- **API 문서**: http://localhost:8080/docs
- **API 기본 URL**: http://localhost:8080/api

### 🔧 개별 서버 실행 (개발용)

#### 백엔드 백그라운드 실행
```bash
cd backend
chmod +x start.sh
./start.sh
```

#### 프론트엔드 백그라운드 실행
```bash
cd frontend
chmod +x start.sh
./start.sh
```

#### 🛑 개별 서버 종료
```bash
# 백엔드 종료
pkill -f "python main.py"

# 프론트엔드 종료
pkill -f "npm run dev"
```

#### 🔍 실행 중인 프로세스 확인
```bash
ps aux | grep -E "(python main.py|npm run dev|vite)"
```

---

## 🎯 주요 기능

### 👤 사용자 관리
- **회원가입/로그인**: JWT 토큰 기반 인증
- **역할 구분**: 멘토(Mentor) / 멘티(Mentee)
- **프로필 관리**: 이름, 소개, 프로필 이미지, 기술 스택

### 🔍 멘토 검색 (멘티 전용)
- **멘토 리스트**: 전체 멘토 목록 조회
- **기술 스택 필터링**: 특정 기술로 멘토 검색
- **정렬**: 이름순/기술순 정렬

### 💌 매칭 시스템
- **매칭 요청**: 멘티 → 멘토 요청 보내기
- **요청 관리**: 수락/거절/취소
- **상태 추적**: pending, accepted, rejected, cancelled

---

## 🏗️ 기술 스택

### 백엔드
- **FastAPI**: Python 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite**: 데이터베이스
- **JWT**: 인증
- **Uvicorn**: ASGI 서버

### 프론트엔드
- **React 18**: UI 라이브러리
- **Vite**: 빌드 도구
- **CSS3**: 스타일링
- **Fetch API**: HTTP 클라이언트

---

## 📁 프로젝트 구조

```
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 서버 파일
│   ├── requirements.txt    # Python 의존성
│   ├── start.sh            # 서버 시작 스크립트
│   ├── create_test_data.py # 테스트 데이터 생성
│   └── list_users.py       # 사용자 목록 확인
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── App.jsx         # 메인 애플리케이션
│   │   ├── main.jsx        # 엔트리 포인트
│   │   └── index.css       # 전역 스타일
│   ├── package.json        # Node.js 의존성
│   ├── vite.config.js      # Vite 설정
│   └── start.sh            # 클라이언트 시작 스크립트
├── docs/                   # 문서
│   ├── mentor-mentee-api-spec.md
│   ├── mentor-mentee-app-requirements.md
│   ├── mentor-mentee-app-user-stories.md
│   ├── mentor-mentee-app-assessment.md
│   ├── openapi.yaml
│   └── test-plan.md
├── test_api.sh             # API 자동화 테스트
├── API_TEST_EVALUATION.md  # API 테스트 결과
├── UI_TEST_EVALUATION.md   # UI 테스트 결과
├── FINAL_EVALUATION.md     # 최종 평가 결과
└── README.md               # 프로젝트 설명
```

---

## 🧪 테스트

### API 테스트 실행
```bash
chmod +x test_api.sh
./test_api.sh
```

### 테스트 결과
- **총 테스트**: 23개
- **성공**: 22개 (95.7%)
- **API 명세서 준수**: 100%

---

## 👥 테스트 계정

### 멘토 계정
- **Sarah Kim**: sarah.kim@example.com / password123
- **David Lee**: david.lee@example.com / password123

### 멘티 계정  
- **Alex Park**: alex.park@example.com / password123
- **Emily Chen**: emily.chen@example.com / password123
- **Michael Wong**: michael.wong@example.com / password123
- **Jessica Liu**: jessica.liu@example.com / password123
- **Ryan Smith**: ryan.smith@example.com / password123
- **Sofia Garcia**: sofia.garcia@example.com / password123

---

## 📊 API 엔드포인트

### 인증
- `POST /api/signup` - 회원가입
- `POST /api/login` - 로그인

### 사용자 정보
- `GET /api/me` - 내 정보 조회
- `GET /api/profile` - 프로필 조회
- `PUT /api/profile` - 프로필 수정
- `GET /api/images/{role}/{id}` - 프로필 이미지

### 멘토 리스트
- `GET /api/mentors` - 멘토 목록 조회 (멘티 전용)

### 매칭 요청
- `POST /api/match-requests` - 매칭 요청 생성
- `GET /api/match-requests/incoming` - 받은 요청 목록 (멘토)
- `GET /api/match-requests/outgoing` - 보낸 요청 목록 (멘티)
- `PUT /api/match-requests/{id}/accept` - 요청 수락 (멘토)
- `PUT /api/match-requests/{id}/reject` - 요청 거절 (멘토)
- `DELETE /api/match-requests/{id}` - 요청 취소 (멘티)

---

## 🏆 평가 결과

### ✅ API 테스트 - **통과**
- 성공률: 95.7% (22/23)
- 모든 핵심 기능 정상 동작
- HTTP 상태 코드 정확한 처리

### ✅ UI 테스트 - **통과**  
- 프론트엔드 + 백엔드 완벽 연동
- 모든 사용자 스토리 구현
- 반응형 웹 디자인

### 🎉 **결선 진출 자격 획득!**

---

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 GitHub Issues를 이용해 주세요.

---

*Made with ❤️ for LipCoding 2025*
