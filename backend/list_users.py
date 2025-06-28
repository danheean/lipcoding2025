#!/usr/bin/env python3
"""
데이터베이스의 사용자 목록을 확인하는 스크립트
"""

import sys
import os

# 스크립트가 있는 디렉토리를 기준으로 경로 설정 (GitHub Actions 대응)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

print(f"👥 사용자 목록 조회")
print(f"현재 작업 디렉토리: {os.getcwd()}")
print("")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User
import json

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./mentor_mentee.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def list_users():
    """데이터베이스의 모든 사용자를 조회합니다."""
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        print(f"=== 데이터베이스 사용자 목록 (총 {len(users)}명) ===\n")
        
        mentors = [user for user in users if user.role == "mentor"]
        mentees = [user for user in users if user.role == "mentee"]
        
        print(f"멘토: {len(mentors)}명")
        for mentor in mentors:
            skills = json.loads(mentor.skills) if mentor.skills else []
            print(f"  ID: {mentor.id}")
            print(f"  이름: {mentor.name}")
            print(f"  이메일: {mentor.email}")
            print(f"  소개: {mentor.bio}")
            print(f"  기술: {', '.join(skills)}")
            print(f"  가입일: {mentor.created_at}")
            print()
        
        print(f"멘티: {len(mentees)}명")
        for mentee in mentees:
            skills = json.loads(mentee.skills) if mentee.skills else []
            print(f"  ID: {mentee.id}")
            print(f"  이름: {mentee.name}")
            print(f"  이메일: {mentee.email}")
            print(f"  소개: {mentee.bio}")
            print(f"  기술: {', '.join(skills)}")
            print(f"  가입일: {mentee.created_at}")
            print()
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
