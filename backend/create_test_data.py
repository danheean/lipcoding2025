#!/usr/bin/env python3
"""
테스트 데이터 생성 스크립트
2명의 멘토와 각 멘토당 3명의 멘티를 생성합니다.
"""

import sys
import os

# 스크립트가 있는 디렉토리를 기준으로 경로 설정 (GitHub Actions 대응)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

print(f"🔧 테스트 데이터 생성 스크립트")
print(f"현재 작업 디렉토리: {os.getcwd()}")
print(f"스크립트 디렉토리: {SCRIPT_DIR}")
print("")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from main import User, Base, get_password_hash

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./mentor_mentee.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_data():
    """테스트 데이터를 생성합니다."""
    db = SessionLocal()
    
    try:
        # 멘토 데이터
        mentors_data = [
            {
                "email": "sarah.kim@example.com",
                "password": "password123",
                "name": "Sarah Kim",
                "role": "mentor",
                "bio": "Senior Software Engineer with 8 years of experience in full-stack development. Passionate about mentoring junior developers and sharing knowledge about React, Node.js, and system design.",
                "skills": '["JavaScript", "React", "Node.js", "Python", "System Design", "AWS", "MongoDB"]'
            },
            {
                "email": "david.lee@example.com", 
                "password": "password123",
                "name": "David Lee",
                "role": "mentor",
                "bio": "Tech Lead and Product Manager with 10+ years in the industry. Expert in agile methodologies, team leadership, and building scalable web applications. Love helping others grow their careers.",
                "skills": '["Leadership", "Product Management", "Java", "Spring Boot", "Microservices", "Docker", "Kubernetes", "PostgreSQL"]'
            }
        ]
        
        # 멘티 데이터 (각 멘토당 3명씩)
        mentees_data = [
            # Sarah Kim의 멘티들
            {
                "email": "alex.park@example.com",
                "password": "password123",
                "name": "Alex Park",
                "role": "mentee",
                "bio": "Computer Science student looking to learn web development. Particularly interested in React and modern JavaScript frameworks.",
                "skills": '["HTML", "CSS", "JavaScript", "Git"]'
            },
            {
                "email": "emily.chen@example.com",
                "password": "password123", 
                "name": "Emily Chen",
                "role": "mentee",
                "bio": "Recent bootcamp graduate seeking guidance in full-stack development. Eager to learn best practices and industry standards.",
                "skills": '["JavaScript", "React", "Node.js", "Express"]'
            },
            {
                "email": "michael.wong@example.com",
                "password": "password123",
                "name": "Michael Wong",
                "role": "mentee", 
                "bio": "Junior developer with 1 year experience. Looking to improve coding skills and learn about system architecture.",
                "skills": '["Python", "Django", "SQL", "JavaScript"]'
            },
            # David Lee의 멘티들
            {
                "email": "jessica.liu@example.com",
                "password": "password123",
                "name": "Jessica Liu",
                "role": "mentee",
                "bio": "Career changer from marketing to tech. Interested in learning about product management and technical leadership.",
                "skills": '["Product Strategy", "User Research", "SQL", "Python"]'
            },
            {
                "email": "ryan.smith@example.com",
                "password": "password123",
                "name": "Ryan Smith", 
                "role": "mentee",
                "bio": "Software engineer looking to transition into technical leadership roles. Seeking guidance on team management and architecture decisions.",
                "skills": '["Java", "Spring", "MySQL", "Docker"]'
            },
            {
                "email": "sofia.garcia@example.com",
                "password": "password123",
                "name": "Sofia Garcia",
                "role": "mentee",
                "bio": "Mid-level developer interested in learning about microservices architecture and cloud technologies.",
                "skills": '["Java", "Spring Boot", "REST APIs", "Git"]'
            }
        ]
        
        # 기존 사용자 확인 및 삭제 (중복 방지)
        existing_emails = [user["email"] for user in mentors_data + mentees_data]
        existing_users = db.query(User).filter(User.email.in_(existing_emails)).all()
        
        if existing_users:
            print(f"기존 테스트 사용자 {len(existing_users)}명을 발견했습니다. 삭제 후 새로 생성합니다.")
            for user in existing_users:
                db.delete(user)
            db.commit()
        
        # 멘토 생성
        created_mentors = []
        for mentor_data in mentors_data:
            mentor = User(
                email=mentor_data["email"],
                hashed_password=get_password_hash(mentor_data["password"]),
                name=mentor_data["name"],
                role=mentor_data["role"],
                bio=mentor_data["bio"],
                skills=mentor_data["skills"],
                created_at=datetime.utcnow()
            )
            db.add(mentor)
            db.flush()  # ID를 얻기 위해 flush
            created_mentors.append(mentor)
            print(f"멘토 생성: {mentor.name} (ID: {mentor.id})")
        
        # 멘티 생성
        created_mentees = []
        for i, mentee_data in enumerate(mentees_data):
            mentee = User(
                email=mentee_data["email"],
                hashed_password=get_password_hash(mentee_data["password"]),
                name=mentee_data["name"],
                role=mentee_data["role"],
                bio=mentee_data["bio"],
                skills=mentee_data["skills"],
                created_at=datetime.utcnow()
            )
            db.add(mentee)
            db.flush()  # ID를 얻기 위해 flush
            created_mentees.append(mentee)
            
            # 어떤 멘토의 멘티인지 표시
            mentor_index = i // 3  # 3명씩 그룹핑
            mentor_name = created_mentors[mentor_index].name
            print(f"멘티 생성: {mentee.name} (ID: {mentee.id}) - {mentor_name}의 멘티")
        
        # 모든 변경사항 커밋
        db.commit()
        
        print("\n=== 테스트 데이터 생성 완료 ===")
        print(f"멘토: {len(created_mentors)}명")
        print(f"멘티: {len(created_mentees)}명")
        print(f"총 사용자: {len(created_mentors) + len(created_mentees)}명")
        
        print("\n=== 로그인 정보 ===")
        print("모든 사용자의 비밀번호: password123")
        print("\n멘토 계정:")
        for mentor in created_mentors:
            print(f"  - {mentor.email} (이름: {mentor.name})")
        
        print("\n멘티 계정:")
        for i, mentee in enumerate(created_mentees):
            mentor_index = i // 3
            mentor_name = created_mentors[mentor_index].name
            print(f"  - {mentee.email} (이름: {mentee.name}) - {mentor_name}의 멘티")
        
        print("\n웹사이트에서 이 계정들로 로그인해서 테스트할 수 있습니다!")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
