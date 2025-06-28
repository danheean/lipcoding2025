#!/usr/bin/env python3
"""
멘토-멘티 매칭 앱 테스트용 매칭 요청 데이터 생성 스크립트
"""

import sqlite3
from datetime import datetime

def create_test_match_requests():
    # 데이터베이스 연결
    conn = sqlite3.connect('mentor_mentee.db')
    cursor = conn.cursor()
    
    # 기존 매칭 요청 데이터 삭제 (테스트용)
    cursor.execute("DELETE FROM match_requests")
    
    # 테스트 매칭 요청 데이터
    test_requests = [
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 13,  # Alex Park
            'message': '안녕하세요! React와 JavaScript를 배우고 싶어서 연락드립니다. 프론트엔드 개발에 대해 멘토링을 받고 싶습니다.',
            'status': 'accepted'
        },
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 14,  # Emily Chen
            'message': 'Full-stack 개발에 대해 배우고 싶습니다. 특히 Node.js와 시스템 설계에 대해 조언을 구하고 싶어요.',
            'status': 'accepted'
        },
        {
            'mentor_id': 12,  # David Lee
            'mentee_id': 16,  # Jessica Liu
            'message': '마케팅에서 테크로 커리어 전환을 준비 중입니다. 프로덕트 매니지먼트에 대해 배우고 싶어요.',
            'status': 'accepted'
        },
        {
            'mentor_id': 12,  # David Lee
            'mentee_id': 17,  # Ryan Smith
            'message': '개발팀 리드 역할을 준비하고 있습니다. 팀 매니지먼트와 리더십에 대해 멘토링 받고 싶습니다.',
            'status': 'accepted'
        },
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 15,  # Michael Wong
            'message': '시스템 아키텍처와 확장성에 대해 깊이 있게 배우고 싶습니다. 멘토링 부탁드립니다.',
            'status': 'pending'
        },
        {
            'mentor_id': 12,  # David Lee
            'mentee_id': 18,  # Sofia Garcia
            'message': '마이크로서비스와 클라우드 기술에 대해 배우고 싶어서 연락드립니다.',
            'status': 'pending'
        },
        {
            'mentor_id': 11,  # Sarah Kim
            'mentee_id': 18,  # Sofia Garcia  
            'message': 'React와 프론트엔드 아키텍처에 대해서도 배우고 싶습니다. 추가 멘토링이 가능한지 문의드립니다.',
            'status': 'rejected'
        }
    ]
    
    # 매칭 요청 데이터 삽입
    for request in test_requests:
        cursor.execute("""
            INSERT INTO match_requests (mentor_id, mentee_id, message, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request['mentor_id'],
            request['mentee_id'],
            request['message'],
            request['status'],
            datetime.now().isoformat()
        ))
    
    conn.commit()
    
    # 생성된 요청 수 확인
    cursor.execute("SELECT COUNT(*) FROM match_requests")
    request_count = cursor.fetchone()[0]
    
    # 결과 출력
    print(f"✅ {request_count}개의 테스트 매칭 요청이 생성되었습니다!")
    print("\n💌 생성된 매칭 요청 목록:")
    
    cursor.execute("""
        SELECT mr.id, mr.status, mr.message, 
               u1.name as mentor_name, u2.name as mentee_name
        FROM match_requests mr
        JOIN users u1 ON mr.mentor_id = u1.id
        JOIN users u2 ON mr.mentee_id = u2.id
        ORDER BY mr.created_at
    """)
    
    requests = cursor.fetchall()
    for request in requests:
        id, status, message, mentor_name, mentee_name = request
        status_emoji = {
            'pending': '⏳',
            'accepted': '✅',
            'rejected': '❌',
            'cancelled': '🚫'
        }.get(status, '❓')
        
        print(f"  {id}: {status_emoji} {status.upper()}")
        print(f"     👤 {mentee_name} → {mentor_name}")
        print(f"     💬 {message[:60]}{'...' if len(message) > 60 else ''}")
        print()
    
    conn.close()
    
    print("🎯 매칭 요청을 확인해보세요!")
    print("📱 멘토로 로그인: sarah.kim@example.com 또는 david.lee@example.com")
    print("📱 멘티로 로그인: alex.park@example.com, emily.chen@example.com 등")
    print("🔑 모든 계정 비밀번호: password123")

if __name__ == "__main__":
    create_test_match_requests()
