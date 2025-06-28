# 테스트 가이드

## 테스트 시나리오

### 1. 멘토로 로그인해서 멘티 요청 확인하기
1. 웹사이트 접속: http://localhost:3001
2. 멘토 계정으로 로그인:
   - 이메일: `sarah.kim@example.com` 또는 `david.lee@example.com`
   - 비밀번호: `password123`
3. Profile 탭에서 프로필 정보 확인
4. Match Requests 탭에서 받은 요청들 확인

### 2. 멘티로 로그인해서 멘토에게 요청 보내기
1. 로그아웃 후 멘티 계정으로 로그인:
   - 이메일: `alex.park@example.com` (또는 다른 멘티 계정)
   - 비밀번호: `password123`
2. Mentors 탭에서 멘토 목록 확인
3. 원하는 멘토에게 "Request Mentorship" 버튼으로 요청 보내기
4. Match Requests 탭에서 보낸 요청 확인

### 3. 프로필 수정하기
1. Profile 탭에서 Edit Profile 버튼 클릭
2. 이름, 소개 등 수정 후 Save Changes
3. 멘토인 경우 기술스택도 수정 가능

### 4. 필터링 기능 테스트
1. Mentors 탭에서 기술스택으로 필터링 테스트
2. 이름/스킬 정렬 기능 테스트

## 데이터베이스 관리

### 테스트 데이터 재생성
```bash
cd backend
python create_test_data.py
```

### 사용자 목록 확인
```bash
cd backend  
python list_users.py
```

### 데이터베이스 초기화
```bash
cd backend
rm mentor_mentee.db
python main.py  # 테이블 재생성
python create_test_data.py  # 테스트 데이터 생성
```

## API 테스트 (Swagger UI)
1. 백엔드 Swagger UI 접속: http://localhost:8080/docs
2. 각 엔드포인트 테스트 가능
3. 인증이 필요한 엔드포인트는 먼저 `/api/login`으로 토큰 획득 후 Authorize 버튼으로 설정

## 트러블슈팅

### 포트 충돌 해결
```bash
# 백엔드 포트 8080 사용 중인 프로세스 종료
lsof -ti:8080 | xargs kill -9

# 프론트엔드 포트 3000 사용 중인 프로세스 종료  
lsof -ti:3000 | xargs kill -9
```

### 로그인 오류 시
1. 브라우저 개발자 도구 Network 탭에서 요청/응답 확인
2. 백엔드 콘솔에서 에러 로그 확인
3. 데이터베이스 초기화 후 재시도
