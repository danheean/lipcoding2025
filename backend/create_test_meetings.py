#!/usr/bin/env python3
"""
멘토-멘티 매칭 앱 테스트용 미팅 데이터 생성 스크립트
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_test_meetings():
    # 데이터베이스 연결
    conn = sqlite3.connect('mentor_mentee.db')
    cursor = conn.cursor()
    
    # 기존 미팅 데이터 삭제 (테스트용)
    cursor.execute("DELETE FROM meetings")
    
    # 오늘 날짜 기준으로 테스트 미팅 생성
    today = datetime.now()
    
    # 테스트 미팅 데이터
    test_meetings = [
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 13,  # Alex Park
            'title': 'React 기초 멘토링',
            'description': 'React 컴포넌트와 Hook 사용법에 대해 배우는 시간',
            'start_time': today + timedelta(days=1, hours=14),  # 내일 오후 2시
            'end_time': today + timedelta(days=1, hours=15),    # 내일 오후 3시
            'status': 'scheduled',
            'meeting_link': 'https://zoom.us/j/1234567890'
        },
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 14,  # Emily Chen
            'title': 'Node.js 백엔드 개발',
            'description': 'Express.js를 활용한 REST API 개발 실습',
            'start_time': today + timedelta(days=2, hours=10),  # 모레 오전 10시
            'end_time': today + timedelta(days=2, hours=11, minutes=30),  # 모레 오전 11시 30분
            'status': 'scheduled',
            'meeting_link': 'https://meet.google.com/abc-defg-hij'
        },
        {
            'mentor_id': 12,  # David Lee
            'mentee_id': 16,  # Jessica Liu
            'title': '프로덕트 매니지먼트 입문',
            'description': '제품 기획과 사용자 리서치 방법론 학습',
            'start_time': today + timedelta(days=3, hours=16),  # 3일 후 오후 4시
            'end_time': today + timedelta(days=3, hours=17),    # 3일 후 오후 5시
            'status': 'scheduled',
            'meeting_link': 'https://teams.microsoft.com/l/meetup-join/xyz'
        },
        {
            'mentor_id': 12,  # David Lee
            'mentee_id': 17,  # Ryan Smith
            'title': '팀 리더십과 기술 매니지먼트',
            'description': '개발팀을 이끄는 리더가 되기 위한 필수 스킬',
            'start_time': today + timedelta(days=5, hours=11),  # 5일 후 오전 11시
            'end_time': today + timedelta(days=5, hours=12, minutes=30),  # 5일 후 오후 12시 30분
            'status': 'scheduled',
            'meeting_link': 'https://zoom.us/j/9876543210'
        },
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 15,  # Michael Wong
            'title': '시스템 아키텍처 설계',
            'description': '확장 가능한 웹 애플리케이션 아키텍처 설계 원칙',
            'start_time': today + timedelta(days=7, hours=15),  # 일주일 후 오후 3시
            'end_time': today + timedelta(days=7, hours=16, minutes=30),  # 일주일 후 오후 4시 30분
            'status': 'scheduled',
            'meeting_link': 'https://zoom.us/j/5555666777'
        },
        {
            'mentor_id': 12,  # David Lee
            'mentee_id': 18,  # Sofia Garcia
            'title': '마이크로서비스 아키텍처',
            'description': 'Docker와 Kubernetes를 활용한 마이크로서비스 구축',
            'start_time': today + timedelta(days=-2, hours=14),  # 2일 전 (완료된 미팅)
            'end_time': today + timedelta(days=-2, hours=15, minutes=30),
            'status': 'completed',
            'meeting_link': 'https://meet.google.com/completed-meeting'
        },
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 13,  # Alex Park
            'title': 'JavaScript 심화 학습',
            'description': 'ES6+ 문법과 비동기 프로그래밍',
            'start_time': today + timedelta(days=-5, hours=10),  # 5일 전 (완료된 미팅)
            'end_time': today + timedelta(days=-5, hours=11, minutes=30),
            'status': 'completed',
            'meeting_link': 'https://zoom.us/j/completed-123'
        }
    ]
    
    # 미팅 데이터 삽입
    for meeting in test_meetings:
        cursor.execute("""
            INSERT INTO meetings (mentor_id, mentee_id, title, description, start_time, end_time, status, meeting_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            meeting['mentor_id'],
            meeting['mentee_id'],
            meeting['title'],
            meeting['description'],
            meeting['start_time'].isoformat(),
            meeting['end_time'].isoformat(),
            meeting['status'],
            meeting['meeting_link']
        ))
    
    conn.commit()
    
    # 생성된 미팅 수 확인
    cursor.execute("SELECT COUNT(*) FROM meetings")
    meeting_count = cursor.fetchone()[0]
    
    # 결과 출력
    print(f"✅ {meeting_count}개의 테스트 미팅이 생성되었습니다!")
    print("\n📅 생성된 미팅 목록:")
    
    cursor.execute("""
        SELECT m.id, m.title, m.start_time, m.status, 
               u1.name as mentor_name, u2.name as mentee_name
        FROM meetings m
        JOIN users u1 ON m.mentor_id = u1.id
        JOIN users u2 ON m.mentee_id = u2.id
        ORDER BY m.start_time
    """)
    
    meetings = cursor.fetchall()
    for meeting in meetings:
        id, title, start_time, status, mentor_name, mentee_name = meeting
        start_dt = datetime.fromisoformat(start_time)
        print(f"  {id}: {title}")
        print(f"     📅 {start_dt.strftime('%Y-%m-%d %H:%M')} ({status})")
        print(f"     👤 {mentor_name} (멘토) ↔ {mentee_name} (멘티)")
        print()
    
    conn.close()
    
    print("🎯 캘린더에서 미팅 일정을 확인해보세요!")
    print("📱 로그인 후 http://localhost:3000 에서 캘린더를 확인할 수 있습니다.")

if __name__ == "__main__":
    create_test_meetings()
