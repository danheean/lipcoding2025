import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Calendar = ({ user }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [meetings, setMeetings] = useState({});
  const [selectedDate, setSelectedDate] = useState(null);
  const [showMeetingForm, setShowMeetingForm] = useState(false);
  const [newMeeting, setNewMeeting] = useState({
    title: '',
    description: '',
    startTime: '',
    endTime: '',
    mentorId: user?.role === 'mentor' ? user.id : '',
    menteeId: user?.role === 'mentee' ? user.id : ''
  });

  useEffect(() => {
    fetchCalendarData();
  }, [currentDate]);

  const fetchCalendarData = async () => {
    try {
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1;
      const response = await axios.get(`/meetings/calendar/${year}/${month}`);
      setMeetings(response.data);
    } catch (error) {
      console.error('Failed to fetch calendar data:', error);
    }
  };

  const getDaysInMonth = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());

    const days = [];
    const endDate = new Date(startDate);
    endDate.setDate(endDate.getDate() + 41); // 6주 표시

    for (let date = new Date(startDate); date <= endDate; date.setDate(date.getDate() + 1)) {
      days.push(new Date(date));
    }

    return days;
  };

  const formatDate = (date) => {
    return date.toISOString().split('T')[0];
  };

  const isToday = (date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isCurrentMonth = (date) => {
    return date.getMonth() === currentDate.getMonth();
  };

  const handleDateClick = (date) => {
    setSelectedDate(date);
  };

  const handlePrevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const handleCreateMeeting = async (e) => {
    e.preventDefault();
    try {
      const meetingData = {
        ...newMeeting,
        startTime: new Date(newMeeting.startTime).toISOString(),
        endTime: new Date(newMeeting.endTime).toISOString()
      };

      await axios.post('/meetings', meetingData);
      setShowMeetingForm(false);
      setNewMeeting({
        title: '',
        description: '',
        startTime: '',
        endTime: '',
        mentorId: user?.role === 'mentor' ? user.id : '',
        menteeId: user?.role === 'mentee' ? user.id : ''
      });
      fetchCalendarData();
    } catch (error) {
      console.error('Failed to create meeting:', error);
      alert('미팅 생성에 실패했습니다.');
    }
  };

  const days = getDaysInMonth();
  const monthNames = [
    '1월', '2월', '3월', '4월', '5월', '6월',
    '7월', '8월', '9월', '10월', '11월', '12월'
  ];
  const dayNames = ['일', '월', '화', '수', '목', '금', '토'];

  return (
    <div className="calendar-container">
      <div className="calendar-header">
        <h2>📅 멘토링 캘린더</h2>
        <div className="calendar-controls">
          <button className="btn btn-secondary" onClick={handlePrevMonth}>
            ◀
          </button>
          <span className="current-month">
            {currentDate.getFullYear()}년 {monthNames[currentDate.getMonth()]}
          </span>
          <button className="btn btn-secondary" onClick={handleNextMonth}>
            ▶
          </button>
        </div>
        <button 
          className="btn btn-primary"
          onClick={() => setShowMeetingForm(true)}
        >
          미팅 추가
        </button>
      </div>

      <div className="calendar-weekdays">
        {dayNames.map(day => (
          <div key={day} className="weekday">{day}</div>
        ))}
      </div>

      <div className="calendar-grid">
        {days.map(date => {
          const dateKey = formatDate(date);
          const dayMeetings = meetings[dateKey] || [];
          
          return (
            <div
              key={dateKey}
              className={`calendar-day ${
                isToday(date) ? 'today' : ''
              } ${
                isCurrentMonth(date) ? '' : 'other-month'
              } ${
                selectedDate && formatDate(selectedDate) === dateKey ? 'selected' : ''
              }`}
              onClick={() => handleDateClick(date)}
            >
              <div className="day-number">{date.getDate()}</div>
              <div className="day-meetings">
                {dayMeetings.slice(0, 2).map((meeting, index) => (
                  <div key={index} className={`meeting-dot ${meeting.status}`}>
                    <span className="meeting-title">{meeting.title}</span>
                    <span className="meeting-time">{meeting.startTime}</span>
                  </div>
                ))}
                {dayMeetings.length > 2 && (
                  <div className="more-meetings">+{dayMeetings.length - 2}</div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {selectedDate && (
        <div className="selected-date-info">
          <h3>{formatDate(selectedDate)} 일정</h3>
          <div className="day-meetings-detail">
            {(meetings[formatDate(selectedDate)] || []).map((meeting, index) => (
              <div key={index} className="meeting-item">
                <div className="meeting-header">
                  <h4>{meeting.title}</h4>
                  <span className={`status ${meeting.status}`}>
                    {meeting.status === 'scheduled' ? '예정' : 
                     meeting.status === 'completed' ? '완료' : '취소'}
                  </span>
                </div>
                <div className="meeting-time">
                  {meeting.startTime} - {meeting.endTime}
                </div>
                <div className="meeting-participant">
                  {meeting.otherUser.name} ({meeting.otherUser.role === 'mentor' ? '멘토' : '멘티'})
                </div>
              </div>
            ))}
            {(meetings[formatDate(selectedDate)] || []).length === 0 && (
              <p>이 날에는 예정된 미팅이 없습니다.</p>
            )}
          </div>
        </div>
      )}

      {showMeetingForm && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>새 미팅 추가</h3>
              <button 
                className="close-btn"
                onClick={() => setShowMeetingForm(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleCreateMeeting}>
              <div className="form-group">
                <label>미팅 제목</label>
                <input
                  type="text"
                  className="form-input"
                  value={newMeeting.title}
                  onChange={(e) => setNewMeeting({...newMeeting, title: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>설명</label>
                <textarea
                  className="form-textarea"
                  value={newMeeting.description}
                  onChange={(e) => setNewMeeting({...newMeeting, description: e.target.value})}
                />
              </div>
              
              <div className="form-group">
                <label>시작 시간</label>
                <input
                  type="datetime-local"
                  className="form-input"
                  value={newMeeting.startTime}
                  onChange={(e) => setNewMeeting({...newMeeting, startTime: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>종료 시간</label>
                <input
                  type="datetime-local"
                  className="form-input"
                  value={newMeeting.endTime}
                  onChange={(e) => setNewMeeting({...newMeeting, endTime: e.target.value})}
                  required
                />
              </div>

              {user?.role === 'mentor' && (
                <div className="form-group">
                  <label>멘티 ID</label>
                  <input
                    type="number"
                    className="form-input"
                    value={newMeeting.menteeId}
                    onChange={(e) => setNewMeeting({...newMeeting, menteeId: parseInt(e.target.value)})}
                    required
                  />
                </div>
              )}

              {user?.role === 'mentee' && (
                <div className="form-group">
                  <label>멘토 ID</label>
                  <input
                    type="number"
                    className="form-input"
                    value={newMeeting.mentorId}
                    onChange={(e) => setNewMeeting({...newMeeting, mentorId: parseInt(e.target.value)})}
                    required
                  />
                </div>
              )}
              
              <div className="form-actions">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setShowMeetingForm(false)}
                >
                  취소
                </button>
                <button type="submit" className="btn btn-primary">
                  미팅 생성
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Calendar;
