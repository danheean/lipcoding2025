from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import os
import base64
import json
from pydantic import BaseModel, EmailStr
import uuid

# JWT 설정
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer 토큰 스키마
security = HTTPBearer(auto_error=False)

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./mentor_mentee.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic 모델들
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str  # "mentor" or "mentee"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    name: str
    role: str
    bio: str
    image: Optional[str] = None
    skills: Optional[List[str]] = None

class MatchRequestCreate(BaseModel):
    mentorId: int
    message: str

class MeetingCreate(BaseModel):
    mentorId: int
    menteeId: int
    title: str
    description: Optional[str] = ""
    startTime: datetime
    endTime: datetime
    meetingLink: Optional[str] = ""

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    status: Optional[str] = None
    meetingLink: Optional[str] = None

# SQLAlchemy 모델들
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    role = Column(String)  # "mentor" or "mentee"
    bio = Column(Text, default="")
    skills = Column(Text, default="")  # JSON string for mentor skills
    profile_image = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)

class MatchRequest(Base):
    __tablename__ = "match_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer)
    mentee_id = Column(Integer)
    message = Column(Text)
    status = Column(String, default="pending")  # pending, accepted, rejected, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer)
    mentee_id = Column(Integer)
    title = Column(String)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    meeting_link = Column(String)  # Zoom, Google Meet 등 링크
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="RiseWith API - 함께 성장하는 멘토링 플랫폼",
    description="함께 일어서고, 함께 성장하는 멘토링 플랫폼 RiseWith의 API 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 이미지 저장을 위한 uploads 디렉토리 생성
os.makedirs("uploads", exist_ok=True)

# 의존성 함수들
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    # RFC 7519 클레임 추가
    to_encode.update({
        "iss": "mentor-mentee-app",  # issuer
        "sub": str(data.get("user_id")),  # subject (user ID)
        "aud": "mentor-mentee-client",  # audience
        "exp": expire,  # expiration time (keep as datetime for python-jose)
        "nbf": now,  # not before
        "iat": now,  # issued at
        "jti": str(uuid.uuid4()),  # JWT ID
        # 추가 사용자 정보
        "email": data.get("email"),
        "name": data.get("name"),
        "role": data.get("role")
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            audience="mentor-mentee-client",
            issuer="mentor-mentee-app"
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception
    
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise credentials_exception
        return user
    except ValueError:
        raise credentials_exception

# API 엔드포인트들

# 루트 엔드포인트 - Swagger UI로 리다이렉트
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# 간단한 테스트 엔드포인트
@app.get("/api/test")
def test_endpoint():
    return {"message": "API is working!", "timestamp": datetime.utcnow()}

@app.get("/api/test-auth")
def test_auth_endpoint(current_user: User = Depends(get_current_user)):
    return {
        "message": "Authentication is working!",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }

# 1. 인증 엔드포인트들
@app.post("/api/signup", status_code=201)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    try:
        # 역할 유효성 검사
        if user.role not in ["mentor", "mentee"]:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'mentor' or 'mentee'")
        
        # 이메일 중복 확인
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # 비밀번호 해싱
        hashed_password = get_password_hash(user.password)
        
        # 사용자 생성
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            name=user.name,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {"message": "User created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        # 사용자 확인
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        # JWT 토큰 생성
        access_token = create_access_token({
            "user_id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "role": db_user.role
        })
        
        return {"token": access_token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# 사용자 정보 반환 헬퍼 함수
def get_current_user_info(user: User):
    """사용자 정보를 API 명세서 형식으로 반환"""
    profile_data = {
        "name": user.name,
        "bio": user.bio,
        "imageUrl": f"/api/images/{user.role}/{user.id}"
    }
    
    # 멘토인 경우 기술스택 추가
    if user.role == "mentor" and user.skills:
        try:
            skills = json.loads(user.skills)
            profile_data["skills"] = skills
        except:
            profile_data["skills"] = []
    
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "profile": profile_data
    }

# 2. 사용자 정보 엔드포인트들
@app.get("/api/me")
def get_me(current_user: User = Depends(get_current_user)):
    """API 명세서 호환성을 위한 /me 엔드포인트"""
    try:
        return get_current_user_info(current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    try:
        return get_current_user_info(current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/images/{role}/{user_id}")
def get_profile_image(role: str, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 프로필 이미지가 있으면 반환, 없으면 기본 이미지 URL로 리다이렉트
        if user.profile_image:
            # 실제 구현에서는 임시 파일로 저장 후 반환
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(user.profile_image)
                tmp.flush()
                return FileResponse(tmp.name, media_type="image/jpeg")
        else:
            # 기본 이미지로 리다이렉트
            if role == "mentor":
                return RedirectResponse("https://placehold.co/500x500.jpg?text=MENTOR", status_code=302)
            else:
                return RedirectResponse("https://placehold.co/500x500.jpg?text=MENTEE", status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/profile")
def update_profile(profile: UserProfile, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # 프로필 업데이트
        current_user.name = profile.name
        current_user.bio = profile.bio
        
        if profile.image:
            try:
                # Base64 이미지 디코딩
                image_data = base64.b64decode(profile.image)
                current_user.profile_image = image_data
            except:
                raise HTTPException(status_code=400, detail="Invalid image format")
        
        if current_user.role == "mentor" and profile.skills:
            current_user.skills = json.dumps(profile.skills)
        
        db.commit()
        
        # 업데이트된 정보 반환
        return get_current_user_info(current_user)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

# 3. 멘토 리스트 조회
@app.get("/api/mentors")
def get_mentors(skill: Optional[str] = None, order_by: Optional[str] = None, 
                current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentee":
            raise HTTPException(status_code=403, detail="Only mentees can access this endpoint")
        
        query = db.query(User).filter(User.role == "mentor")
        
        # 스킬 필터링
        if skill:
            query = query.filter(User.skills.contains(skill.lower()))
        
        mentors = query.all()
        
        # 정렬
        if order_by == "name":
            mentors.sort(key=lambda x: x.name)
        elif order_by == "skill":
            # 스킬 기준 정렬 (첫 번째 스킬 기준)
            def get_first_skill(user):
                try:
                    skills = json.loads(user.skills) if user.skills else []
                    return skills[0] if skills else ""
                except:
                    return ""
            mentors.sort(key=get_first_skill)
        else:
            mentors.sort(key=lambda x: x.id)
        
        result = []
        for mentor in mentors:
            skills = []
            if mentor.skills:
                try:
                    skills = json.loads(mentor.skills)
                except:
                    skills = []
            
            result.append({
                "id": mentor.id,
                "email": mentor.email,
                "role": mentor.role,
                "profile": {
                    "name": mentor.name,
                    "bio": mentor.bio,
                    "imageUrl": f"/api/images/mentor/{mentor.id}",
                    "skills": skills
                }
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# 4. 매칭 요청 엔드포인트들
@app.post("/api/match-requests")
def create_match_request(request: MatchRequestCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentee":
            raise HTTPException(status_code=403, detail="Only mentees can send requests")
        
        # 멘토 존재 확인
        mentor = db.query(User).filter(User.id == request.mentorId, User.role == "mentor").first()
        if not mentor:
            raise HTTPException(status_code=400, detail="Mentor not found")
        
        # 이미 요청이 있는지 확인 (cancelled 상태 제외)
        existing_request = db.query(MatchRequest).filter(
            MatchRequest.mentor_id == request.mentorId,
            MatchRequest.mentee_id == current_user.id,
            MatchRequest.status.in_(["pending", "accepted"])
        ).first()
        
        if existing_request:
            raise HTTPException(status_code=400, detail="Request already exists")
        
        # 요청 생성
        match_request = MatchRequest(
            mentor_id=request.mentorId,
            mentee_id=current_user.id,
            message=request.message
        )
        db.add(match_request)
        db.commit()
        db.refresh(match_request)
        
        return {
            "id": match_request.id,
            "mentorId": match_request.mentor_id,
            "menteeId": match_request.mentee_id,
            "message": match_request.message,
            "status": match_request.status
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/match-requests/incoming")
def get_incoming_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentor":
            raise HTTPException(status_code=403, detail="Only mentors can access this endpoint")
        
        requests = db.query(MatchRequest).filter(MatchRequest.mentor_id == current_user.id).all()
        
        result = []
        for req in requests:
            result.append({
                "id": req.id,
                "mentorId": req.mentor_id,
                "menteeId": req.mentee_id,
                "message": req.message,
                "status": req.status
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/match-requests/outgoing")
def get_outgoing_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentee":
            raise HTTPException(status_code=403, detail="Only mentees can access this endpoint")
        
        requests = db.query(MatchRequest).filter(MatchRequest.mentee_id == current_user.id).all()
        
        result = []
        for req in requests:
            result.append({
                "id": req.id,
                "mentorId": req.mentor_id,
                "menteeId": req.mentee_id,
                "status": req.status
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/match-requests/{request_id}/accept")
def accept_match_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentor":
            raise HTTPException(status_code=403, detail="Only mentors can accept requests")
        
        match_request = db.query(MatchRequest).filter(
            MatchRequest.id == request_id,
            MatchRequest.mentor_id == current_user.id
        ).first()
        
        if not match_request:
            raise HTTPException(status_code=404, detail="Match request not found")
        
        # 다른 요청들을 거절 처리
        other_requests = db.query(MatchRequest).filter(
            MatchRequest.mentor_id == current_user.id,
            MatchRequest.status == "pending",
            MatchRequest.id != request_id
        ).all()
        
        for req in other_requests:
            req.status = "rejected"
        
        match_request.status = "accepted"
        db.commit()
        
        return {
            "id": match_request.id,
            "mentorId": match_request.mentor_id,
            "menteeId": match_request.mentee_id,
            "message": match_request.message,
            "status": match_request.status
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/match-requests/{request_id}/reject")
def reject_match_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentor":
            raise HTTPException(status_code=403, detail="Only mentors can reject requests")
        
        match_request = db.query(MatchRequest).filter(
            MatchRequest.id == request_id,
            MatchRequest.mentor_id == current_user.id
        ).first()
        
        if not match_request:
            raise HTTPException(status_code=404, detail="Match request not found")
        
        match_request.status = "rejected"
        db.commit()
        
        return {
            "id": match_request.id,
            "mentorId": match_request.mentor_id,
            "menteeId": match_request.mentee_id,
            "message": match_request.message,
            "status": match_request.status
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/match-requests/{request_id}")
def cancel_match_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.role != "mentee":
            raise HTTPException(status_code=403, detail="Only mentees can cancel requests")
        
        match_request = db.query(MatchRequest).filter(
            MatchRequest.id == request_id,
            MatchRequest.mentee_id == current_user.id
        ).first()
        
        if not match_request:
            raise HTTPException(status_code=404, detail="Match request not found")
        
        match_request.status = "cancelled"
        db.commit()
        
        return {
            "id": match_request.id,
            "mentorId": match_request.mentor_id,
            "menteeId": match_request.mentee_id,
            "message": match_request.message,
            "status": match_request.status
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

# ========================
# 미팅 관리 API
# ========================

@app.post("/api/meetings")
def create_meeting(meeting: MeetingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # 멘토만 미팅을 생성할 수 있거나, 본인 관련 미팅만 생성 가능
        if current_user.role == "mentor" and meeting.mentorId != current_user.id:
            raise HTTPException(status_code=403, detail="Can only create meetings for yourself")
        elif current_user.role == "mentee" and meeting.menteeId != current_user.id:
            raise HTTPException(status_code=403, detail="Can only create meetings for yourself")
        
        # 시간 충돌 확인
        existing_meeting = db.query(Meeting).filter(
            ((Meeting.mentor_id == meeting.mentorId) | (Meeting.mentee_id == meeting.menteeId)),
            Meeting.status == "scheduled",
            ((Meeting.start_time <= meeting.startTime) & (Meeting.end_time > meeting.startTime)) |
            ((Meeting.start_time < meeting.endTime) & (Meeting.end_time >= meeting.endTime)) |
            ((Meeting.start_time >= meeting.startTime) & (Meeting.end_time <= meeting.endTime))
        ).first()
        
        if existing_meeting:
            raise HTTPException(status_code=400, detail="Time slot conflicts with existing meeting")
        
        db_meeting = Meeting(
            mentor_id=meeting.mentorId,
            mentee_id=meeting.menteeId,
            title=meeting.title,
            description=meeting.description,
            start_time=meeting.startTime,
            end_time=meeting.endTime,
            meeting_link=meeting.meetingLink
        )
        
        db.add(db_meeting)
        db.commit()
        db.refresh(db_meeting)
        
        return {
            "id": db_meeting.id,
            "mentorId": db_meeting.mentor_id,
            "menteeId": db_meeting.mentee_id,
            "title": db_meeting.title,
            "description": db_meeting.description,
            "startTime": db_meeting.start_time.isoformat(),
            "endTime": db_meeting.end_time.isoformat(),
            "status": db_meeting.status,
            "meetingLink": db_meeting.meeting_link,
            "createdAt": db_meeting.created_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/meetings")
def get_meetings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        meetings = db.query(Meeting).filter(
            (Meeting.mentor_id == current_user.id) | (Meeting.mentee_id == current_user.id)
        ).order_by(Meeting.start_time.desc()).all()
        
        result = []
        for meeting in meetings:
            # 상대방 정보 가져오기
            if meeting.mentor_id == current_user.id:
                other_user = db.query(User).filter(User.id == meeting.mentee_id).first()
                other_role = "mentee"
            else:
                other_user = db.query(User).filter(User.id == meeting.mentor_id).first()
                other_role = "mentor"
            
            result.append({
                "id": meeting.id,
                "mentorId": meeting.mentor_id,
                "menteeId": meeting.mentee_id,
                "title": meeting.title,
                "description": meeting.description,
                "startTime": meeting.start_time.isoformat(),
                "endTime": meeting.end_time.isoformat(),
                "status": meeting.status,
                "meetingLink": meeting.meeting_link,
                "createdAt": meeting.created_at.isoformat(),
                "otherUser": {
                    "id": other_user.id if other_user else None,
                    "name": other_user.name if other_user else "Unknown",
                    "email": other_user.email if other_user else "",
                    "role": other_role
                }
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/meetings/calendar/{year}/{month}")
def get_calendar_meetings(year: int, month: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        from calendar import monthrange
        import calendar
        
        # 해당 월의 첫날과 마지막날 계산
        first_day = datetime(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = datetime(year, month, last_day_num, 23, 59, 59)
        
        meetings = db.query(Meeting).filter(
            (Meeting.mentor_id == current_user.id) | (Meeting.mentee_id == current_user.id),
            Meeting.start_time >= first_day,
            Meeting.start_time <= last_day
        ).order_by(Meeting.start_time).all()
        
        # 날짜별로 미팅 그룹화
        calendar_data = {}
        for meeting in meetings:
            date_key = meeting.start_time.strftime('%Y-%m-%d')
            if date_key not in calendar_data:
                calendar_data[date_key] = []
            
            # 상대방 정보 가져오기
            if meeting.mentor_id == current_user.id:
                other_user = db.query(User).filter(User.id == meeting.mentee_id).first()
                other_role = "mentee"
            else:
                other_user = db.query(User).filter(User.id == meeting.mentor_id).first()
                other_role = "mentor"
            
            calendar_data[date_key].append({
                "id": meeting.id,
                "title": meeting.title,
                "startTime": meeting.start_time.strftime('%H:%M'),
                "endTime": meeting.end_time.strftime('%H:%M'),
                "status": meeting.status,
                "otherUser": {
                    "name": other_user.name if other_user else "Unknown",
                    "role": other_role
                }
            })
        
        return calendar_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/meetings/{meeting_id}")
def update_meeting(meeting_id: int, meeting_update: MeetingUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        meeting = db.query(Meeting).filter(
            Meeting.id == meeting_id,
            (Meeting.mentor_id == current_user.id) | (Meeting.mentee_id == current_user.id)
        ).first()
        
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        # 업데이트할 필드들 적용
        if meeting_update.title is not None:
            meeting.title = meeting_update.title
        if meeting_update.description is not None:
            meeting.description = meeting_update.description
        if meeting_update.startTime is not None:
            meeting.start_time = meeting_update.startTime
        if meeting_update.endTime is not None:
            meeting.end_time = meeting_update.endTime
        if meeting_update.status is not None:
            meeting.status = meeting_update.status
        if meeting_update.meetingLink is not None:
            meeting.meeting_link = meeting_update.meetingLink
        
        meeting.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "id": meeting.id,
            "mentorId": meeting.mentor_id,
            "menteeId": meeting.mentee_id,
            "title": meeting.title,
            "description": meeting.description,
            "startTime": meeting.start_time.isoformat(),
            "endTime": meeting.end_time.isoformat(),
            "status": meeting.status,
            "meetingLink": meeting.meeting_link,
            "updatedAt": meeting.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/meetings/{meeting_id}")
def delete_meeting(meeting_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        meeting = db.query(Meeting).filter(
            Meeting.id == meeting_id,
            (Meeting.mentor_id == current_user.id) | (Meeting.mentee_id == current_user.id)
        ).first()
        
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        db.delete(meeting)
        db.commit()
        
        return {"message": "Meeting deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
