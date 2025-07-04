# 📱 RiseWith - 함께 성장하는 멘토링 플랫폼

> **LipCoding 2025** 해커톤 프로젝트 - "함께 일어서고, 함께 성장하는" 모바일 친화적 멘토링 웹 애플리케이션

## 🎉 프로젝트 완성! 

✅ **API 테스트 통과**: 95.7% (22/23 성공)  
✅ **UI 테스트 통과**: 100% 구현  
✅ **API 명세서 준수율**: 100%  
✅ **역할별 테마 시스템**: 멘토(블루) / 멘티(녹색)  
✅ **모바일 친화적 UI**: 반응형 디자인 및 터치 최적화  
✅ **PWA 지원**: 모바일 앱처럼 사용 가능  

---

## 🌟 RiseWith의 의미

**"함께 일어서고, 함께 성장하다"**

- 🌅 **Rise Mentor**: 경험으로 다른 이들의 성공적인 도약을 이끌어주는 멘토
- 🤲 **Rise Together**: 멘토와 손잡고 더 높은 곳으로 함께 올라가는 멘티  
- 🎯 **동반성장**: 가르치고 배우며 서로가 함께 발전하는 선순환 생태계

---

## 📱 모바일 친화성 특징

### 🎨 반응형 디자인
- **모바일 우선 설계**: 768px 이하 모바일 화면 최적화
- **터치 친화적 인터페이스**: 최소 44px 터치 타겟 크기
- **부드러운 애니메이션**: 터치 피드백 및 햅틱 시뮬레이션

### 📲 PWA (Progressive Web App) 기능
- **홈 화면 추가**: 네이티브 앱처럼 설치 가능
- **오프라인 지원**: 기본 기능 캐싱
- **푸시 알림 준비**: 멘토링 요청 및 일정 알림

### 🖱️ 터치 제스처 및 인터랙션
- **스와이프 지원**: 카드 스와이프 제스처
- **터치 피드백**: 버튼 터치 시 시각적 피드백
- **iOS 최적화**: 자동 줌 방지 및 스크롤 최적화

### 📐 모바일 최적화 UI
- **스티키 네비게이션**: 상단 고정 네비게이션 바
- **풀스크린 모달**: 모바일에 최적화된 모달 창
- **반응형 그리드**: 화면 크기에 따른 레이아웃 자동 조정

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

## 🔧 GitHub Actions CI/CD

### 자동화된 테스트 및 배포

이 프로젝트는 GitHub Actions를 통한 완전 자동화된 CI/CD 파이프라인을 제공합니다.

#### 🎯 워크플로우 단계

1. **테스트 단계** (`test`)
   - 백엔드/프론트엔드 의존성 설치
   - 코드 빌드 테스트
   - 전체 시스템 통합 테스트
   - API 엔드포인트 검증

2. **Docker 테스트** (`docker-test`)
   - Docker Compose 빌드
   - 컨테이너 환경 테스트
   - 서비스 간 통신 확인

3. **배포 단계** (`deploy`)
   - main 브랜치 푸시 시 자동 실행
   - 프로덕션 환경 배포

#### 🚀 트리거 조건

- `push`: main, develop 브랜치
- `pull_request`: main 브랜치

#### 📋 로컬에서 GitHub Actions 시뮬레이션

```bash
# 1. 전체 시스템 테스트
./start.sh
sleep 45
./test_api.sh
./test_user_stories.sh
./stop.sh

# 2. Docker 환경 테스트
docker-compose up -d
sleep 60
curl http://localhost:8080/docs
curl http://localhost:3000
docker-compose down
```

#### 🔍 워크플로우 상태 확인

GitHub 저장소의 Actions 탭에서 실시간으로 빌드 상태를 확인할 수 있습니다.

#### ⚙️ 환경 변수 설정

GitHub Secrets에서 다음 변수들을 설정할 수 있습니다:
- `DEPLOY_HOST`: 배포 서버 주소
- `DEPLOY_KEY`: 배포용 SSH 키
- `DOCKER_REGISTRY`: Docker 레지스트리 URL

---

*Made with ❤️ for LipCoding 2025*
