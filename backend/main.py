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
security = HTTPBearer()

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
    menteeId: int
    message: str

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

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="Mentor-Mentee Matching API",
    description="API for matching mentors and mentees in a mentoring platform",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    # RFC 7519 클레임 추가
    to_encode.update({
        "iss": "mentor-mentee-app",  # issuer
        "sub": str(data.get("user_id")),  # subject (user ID)
        "aud": "mentor-mentee-client",  # audience
        "exp": expire,  # expiration time
        "nbf": datetime.utcnow(),  # not before
        "iat": datetime.utcnow(),  # issued at
        "jti": str(uuid.uuid4()),  # JWT ID
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

# API 엔드포인트들

# 루트 엔드포인트 - Swagger UI로 리다이렉트
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# 1. 인증 엔드포인트들
@app.post("/api/signup", status_code=201)
def signup(user: UserSignup, db: Session = Depends(get_db)):
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

@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
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

# 2. 사용자 정보 엔드포인트들
@app.get("/api/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    profile_data = {
        "name": current_user.name,
        "bio": current_user.bio,
        "imageUrl": f"/api/images/{current_user.role}/{current_user.id}"
    }
    
    if current_user.role == "mentor":
        skills = []
        if current_user.skills:
            try:
                skills = json.loads(current_user.skills)
            except:
                skills = []
        profile_data["skills"] = skills
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "profile": profile_data
    }

@app.get("/api/images/{role}/{user_id}")
def get_profile_image(role: str, user_id: int, db: Session = Depends(get_db)):
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
            return RedirectResponse("https://placehold.co/500x500.jpg?text=MENTOR")
        else:
            return RedirectResponse("https://placehold.co/500x500.jpg?text=MENTEE")

@app.put("/api/profile")
def update_profile(profile: UserProfile, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

# 3. 멘토 리스트 조회
@app.get("/api/mentors")
def get_mentors(skill: Optional[str] = None, order_by: Optional[str] = None, 
                current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

# 4. 매칭 요청 엔드포인트들
@app.post("/api/match-requests")
def create_match_request(request: MatchRequestCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "mentee":
        raise HTTPException(status_code=403, detail="Only mentees can send requests")
    
    # 멘토 존재 확인
    mentor = db.query(User).filter(User.id == request.mentorId, User.role == "mentor").first()
    if not mentor:
        raise HTTPException(status_code=400, detail="Mentor not found")
    
    # 이미 요청이 있는지 확인
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

@app.get("/api/match-requests/incoming")
def get_incoming_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

@app.get("/api/match-requests/outgoing")
def get_outgoing_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

@app.put("/api/match-requests/{request_id}/accept")
def accept_match_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

@app.put("/api/match-requests/{request_id}/reject")
def reject_match_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

@app.delete("/api/match-requests/{request_id}")
def cancel_match_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
