import React, { useState, useEffect, createContext, useContext } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Calendar from './Calendar'

// API 기본 설정
const API_BASE = 'http://localhost:8080/api'
axios.defaults.baseURL = API_BASE

// 모바일 감지 유틸리티
const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
         window.innerWidth <= 768
}

// 터치 제스처 훅
const useTouch = (onSwipeLeft, onSwipeRight) => {
  const [touchStart, setTouchStart] = useState(null)
  const [touchEnd, setTouchEnd] = useState(null)

  const minSwipeDistance = 50

  const onTouchStart = (e) => {
    setTouchEnd(null)
    setTouchStart(e.targetTouches[0].clientX)
  }

  const onTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientX)
  }

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return
    const distance = touchStart - touchEnd
    const isLeftSwipe = distance > minSwipeDistance
    const isRightSwipe = distance < -minSwipeDistance

    if (isLeftSwipe && onSwipeLeft) {
      onSwipeLeft()
    }
    if (isRightSwipe && onSwipeRight) {
      onSwipeRight()
    }
  }

  return {
    onTouchStart,
    onTouchMove,
    onTouchEnd
  }
}

// 반응형 훅
const useResponsive = () => {
  const [isMobileView, setIsMobileView] = useState(false)

  useEffect(() => {
    const handleResize = () => {
      setIsMobileView(window.innerWidth <= 768)
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return isMobileView
}

// Context for authentication
const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

// Auth Provider Component
const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUserInfo()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUserInfo = async () => {
    try {
      const response = await axios.get('/profile')
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await axios.post('/login', { email, password })
      const { token } = response.data
      
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      // 토큰 설정 후 사용자 정보 가져오기
      setTimeout(async () => {
        await fetchUserInfo()
      }, 100)
      
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const signup = async (email, password, name, role) => {
    try {
      await axios.post('/signup', { email, password, name, role })
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Signup failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value = {
    user,
    login,
    signup,
    logout,
    loading,
    fetchUserInfo
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Navigation Component
const Navbar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [iconMode, setIconMode] = useState(false)
  const isMobileView = useResponsive()

  // 모바일에서는 기본적으로 아이콘 모드
  useEffect(() => {
    if (isMobileView) {
      setIconMode(true)
    }
  }, [isMobileView])

  const handleLogout = () => {
    if (window.confirm('정말 로그아웃하시겠습니까?')) {
      logout()
      navigate('/')
    }
  }

  if (!user) return null

  // 역할별 브랜드 아이콘과 색상
  const roleConfig = {
    mentor: {
      brandIcon: '🌅',
      brandText: 'RiseWith 멘토',
      profileIcon: '🎓',
      color: 'blue'
    },
    mentee: {
      brandIcon: '🤲',
      brandText: 'RiseWith 새싹',
      profileIcon: '🌿',
      color: 'green'
    }
  }

  const config = roleConfig[user.role]

  return (
    <nav className={`navbar navbar-${config.color} ${iconMode ? 'navbar-icon-mode' : ''}`}>
      <div className="navbar-content">
        <Link 
          to="/" 
          className="navbar-brand clickable touchable" 
          title="RiseWith - 함께 성장하는 플랫폼"
        >
          <span className="brand-icon">{config.brandIcon}</span>
          {!iconMode && <span className="brand-text">{config.brandText}</span>}
        </Link>
        
        {/* 모바일에서는 아이콘 토글 버튼 숨김 */}
        {!isMobileView && (
          <div className="navbar-controls">
            <button 
              onClick={() => setIconMode(!iconMode)} 
              className="icon-toggle-btn clickable touchable"
              title={iconMode ? "텍스트 표시" : "아이콘만 표시"}
            >
              {iconMode ? '📝' : '🎯'}
            </button>
          </div>
        )}

        <div className="navbar-nav">
          <Link 
            to="/profile" 
            title="프로필"
            className="clickable touchable"
          >
            <span className="nav-icon">{config.profileIcon}</span>
            {!iconMode && <span className="nav-text">프로필</span>}
          </Link>
          {user.role === 'mentee' && (
            <Link 
              to="/mentors" 
              title="멘토 찾기"
              className="clickable touchable"
            >
              <span className="nav-icon">🔍</span>
              {!iconMode && <span className="nav-text">멘토 찾기</span>}
            </Link>
          )}
          <Link 
            to="/requests" 
            title={user.role === 'mentor' ? '받은 요청' : '보낸 요청'}
            className="clickable touchable"
          >
            <span className="nav-icon">{user.role === 'mentor' ? '📥' : '📤'}</span>
            {!iconMode && <span className="nav-text">{user.role === 'mentor' ? '받은 요청' : '보낸 요청'}</span>}
          </Link>
          <button 
            onClick={handleLogout} 
            className="btn btn-secondary logout-btn clickable touchable" 
            title="로그아웃"
          >
            <span className="nav-icon">🚪</span>
            {!iconMode && <span className="nav-text">로그아웃</span>}
          </button>
        </div>
      </div>
    </nav>
  )
}

// Login Component
const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await login(email, password)
    
    if (result.success) {
      navigate('/profile')
    } else {
      setError(result.error)
    }
    
    setLoading(false)
  }

  const quickLogin = async (testEmail, testPassword) => {
    setLoading(true)
    setError('')
    setEmail(testEmail)
    setPassword(testPassword)

    const result = await login(testEmail, testPassword)
    
    if (result.success) {
      navigate('/profile')
    } else {
      setError(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '500px', margin: '50px auto' }}>
        <h2 className="text-center mb-4 page-title">
          <span className="title-icon">🔐</span>
          RiseWith 로그인
        </h2>
        
        {/* 역할별 테마 프리뷰 */}
        <div className="theme-preview-container" style={{ marginBottom: '30px' }}>
          <div className="theme-preview-title">
            <span style={{ fontSize: '16px', fontWeight: 'bold', color: '#374151' }}>
              🎨 역할별 테마 미리보기
            </span>
          </div>
          <div className="theme-preview-grid" style={{ 
            display: 'grid', 
            gridTemplateColumns: '1fr 1fr', 
            gap: '15px', 
            marginTop: '15px' 
          }}>
            <div className="theme-preview mentor-preview" style={{
              padding: '15px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
              color: 'white',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '24px', marginBottom: '8px' }}>👨‍🏫</div>
              <div style={{ fontSize: '14px', fontWeight: 'bold' }}>멘토 테마</div>
              <div style={{ fontSize: '12px', opacity: 0.9 }}>블루 계열 (전문가)</div>
            </div>
            <div className="theme-preview mentee-preview" style={{
              padding: '15px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
              color: 'white',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '24px', marginBottom: '8px' }}>🌱</div>
              <div style={{ fontSize: '14px', fontWeight: 'bold' }}>멘티 테마</div>
              <div style={{ fontSize: '12px', opacity: 0.9 }}>녹색 계열 (새싹)</div>
            </div>
          </div>
        </div>
        
        {error && <div className="alert alert-error">{error}</div>}
        
        {/* 로그인 디버그 정보 */}
        {loading && (
          <div style={{ 
            padding: '10px', 
            backgroundColor: '#e3f2fd', 
            borderRadius: '4px', 
            marginBottom: '15px',
            fontSize: '12px',
            color: '#1976d2'
          }}>
            🔄 로그인 중... (이메일: {email})
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>이메일</label>
            <input
              id="email"
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label>비밀번호</label>
            <input
              id="password"
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button id="login" type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? '로그인 중...' : '로그인'}
          </button>
        </form>
        
        {/* 테스트용 빠른 로그인 버튼들 */}
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
          <h4 style={{ fontSize: '14px', color: '#666', marginBottom: '15px' }}>🧪 테스트 계정 빠른 로그인</h4>
          
          <div style={{ display: 'grid', gap: '10px' }}>
            <div style={{ marginBottom: '10px' }}>
              <div style={{ fontSize: '12px', color: '#2563eb', fontWeight: 'bold', marginBottom: '6px' }}>
                👨‍🏫 멘토 계정 (블루 테마)
              </div>
              <button 
                onClick={() => quickLogin('sarah.kim@example.com', 'password123')}
                className="btn"
                style={{ 
                  fontSize: '12px', 
                  padding: '10px', 
                  width: '100%',
                  background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
                  color: 'white',
                  border: 'none',
                  marginBottom: '6px'
                }}
                disabled={loading}
              >
                👩‍💻 Sarah Kim - 풀스택 개발자
              </button>
              
              <button 
                onClick={() => quickLogin('david.lee@example.com', 'password123')}
                className="btn"
                style={{ 
                  fontSize: '12px', 
                  padding: '10px', 
                  width: '100%',
                  background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
                  color: 'white',
                  border: 'none'
                }}
                disabled={loading}
              >
                👨‍💼 David Lee - 테크리드 & PM
              </button>
            </div>
            
            <div>
              <div style={{ fontSize: '12px', color: '#059669', fontWeight: 'bold', marginBottom: '6px' }}>
                🌱 멘티 계정 (녹색 테마)
              </div>
              <button 
                onClick={() => quickLogin('alex.park@example.com', 'password123')}
                className="btn"
                style={{ 
                  fontSize: '12px', 
                  padding: '10px', 
                  width: '100%',
                  background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
                  color: 'white',
                  border: 'none',
                  marginBottom: '6px'
                }}
                disabled={loading}
              >
                🎓 Alex Park - 컴공과 학생
              </button>
              
              <button 
                onClick={() => quickLogin('emily.chen@example.com', 'password123')}
                className="btn"
                style={{ 
                  fontSize: '12px', 
                  padding: '10px', 
                  width: '100%',
                  background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
                  color: 'white',
                  border: 'none'
                }}
              >
                💻 Emily Chen - 부트캠프 졸업생
              </button>
            </div>
          </div>
          
          <p style={{ fontSize: '11px', color: '#888', marginTop: '8px', marginBottom: '0' }}>
            * 모든 테스트 계정의 비밀번호: password123
          </p>
        </div>
        
        <div className="text-center" style={{ marginTop: '20px' }}>
          <Link to="/signup">회원가입</Link>
        </div>
      </div>
    </div>
  )
}

// Signup Component
const Signup = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [role, setRole] = useState('mentee')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signup } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await signup(email, password, name, role)
    
    if (result.success) {
      navigate('/', { state: { message: '회원가입이 완료되었습니다. 로그인해주세요.' } })
    } else {
      setError(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '400px', margin: '100px auto' }}>
        <h2 className="text-center mb-4 page-title">
          <span className="title-icon">✨</span>
          RiseWith 회원가입
        </h2>
        
        {error && <div className="alert alert-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>이메일</label>
            <input
              id="email"
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label>비밀번호</label>
            <input
              id="password"
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label>이름</label>
            <input
              type="text"
              className="form-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label>역할</label>
            <select
              id="role"
              className="form-select"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="mentee">멘티</option>
              <option value="mentor">멘토</option>
            </select>
          </div>
          
          <button id="signup" type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? '가입 중...' : '회원가입'}
          </button>
        </form>
        
        <div className="text-center" style={{ marginTop: '20px' }}>
          <Link to="/">로그인</Link>
        </div>
      </div>
    </div>
  )
}

// Profile Component
const Profile = () => {
  const { user, fetchUserInfo } = useAuth()
  const [name, setName] = useState('')
  const [bio, setBio] = useState('')
  const [skills, setSkills] = useState('')
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (user) {
      setName(user.profile.name || '')
      setBio(user.profile.bio || '')
      if (user.role === 'mentor') {
        setSkills(user.profile.skills ? user.profile.skills.join(', ') : '')
      }
    }
  }, [user])

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setImage(e.target.result.split(',')[1]) // Remove data:image/...;base64, prefix
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const profileData = {
        id: user.id,
        name,
        role: user.role,
        bio,
        image
      }

      if (user.role === 'mentor') {
        profileData.skills = skills.split(',').map(s => s.trim()).filter(s => s)
      }

      await axios.put('/profile', profileData)
      await fetchUserInfo()
      setMessage('프로필이 성공적으로 업데이트되었습니다.')
    } catch (error) {
      setMessage('프로필 업데이트에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  if (!user) return <div className="loading"><div className="spinner"></div></div>

  // 역할별 프로필 설정
  const profileConfig = {
    mentor: {
      titleIcon: '🎓',
      title: 'Rise Mentor 프로필',
      subtitle: '경험을 나누며 함께 성장의 여정을 이끌어주세요'
    },
    mentee: {
      titleIcon: '🌿',
      title: 'Rise Together 프로필', 
      subtitle: '멘토와 함께 더 높은 곳으로 올라가세요'
    }
  }

  const config = profileConfig[user.role]

  return (
    <div className="container">
      {/* 캘린더 섹션 - 로그인 후 첫 화면 */}
      <Calendar user={user} />
      
      <div className="card">
        <h2 className="mb-4 page-title">
          <span className="title-icon">{config.titleIcon}</span>
          {config.title}
        </h2>
        <p style={{ 
          textAlign: 'center', 
          color: 'var(--text-primary)', 
          marginBottom: '30px',
          fontSize: '16px',
          fontStyle: 'italic'
        }}>
          {config.subtitle}
        </p>
        
        {message && (
          <div className={`alert ${message.includes('실패') ? 'alert-error' : 'alert-success'}`}>
            {message}
          </div>
        )}
        
        <div className="grid grid-2">
          <div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>이름</label>
                <input
                  id="name"
                  type="text"
                  className="form-input"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>소개</label>
                <textarea
                  id="bio"
                  className="form-textarea"
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                  placeholder="자신을 소개해주세요..."
                />
              </div>
              
              {user.role === 'mentor' && (
                <div className="form-group">
                  <label>기술 스택 (쉼표로 구분)</label>
                  <input
                    id="skillsets"
                    type="text"
                    className="form-input"
                    value={skills}
                    onChange={(e) => setSkills(e.target.value)}
                    placeholder="React, Vue, Node.js"
                  />
                </div>
              )}
              
              <div className="form-group">
                <label>프로필 이미지</label>
                <input
                  id="profile"
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="form-input"
                />
              </div>
              
              <button id="save" type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? '저장 중...' : '프로필 저장'}
              </button>
            </form>
          </div>
          
          <div>
            <h3 className="mb-4 section-title">
              <span className="title-icon">👁️</span>
              프로필 미리보기
            </h3>
            <div className="mentor-card">
              <img
                id="profile-photo"
                src={user.profile.imageUrl}
                alt="Profile"
                className="mentor-avatar"
              />
              <div className="mentor-name">{name || user.profile.name}</div>
              <div className="mentor-bio">{bio || user.profile.bio}</div>
              {user.role === 'mentor' && (
                <div className="skills">
                  {(skills ? skills.split(',').map(s => s.trim()) : user.profile.skills || []).map((skill, index) => (
                    <span key={index} className="skill-tag">{skill}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// Mentors List Component (for mentees)
const Mentors = () => {
  const { user } = useAuth()
  const [mentors, setMentors] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchSkill, setSearchSkill] = useState('')
  const [orderBy, setOrderBy] = useState('')

  useEffect(() => {
    fetchMentors()
  }, [searchSkill, orderBy])

  const fetchMentors = async () => {
    try {
      const params = {}
      if (searchSkill) params.skill = searchSkill
      if (orderBy) params.order_by = orderBy

      const response = await axios.get('/mentors', { params })
      setMentors(response.data)
    } catch (error) {
      console.error('Failed to fetch mentors:', error)
    } finally {
      setLoading(false)
    }
  }

  const sendRequest = async (mentorId) => {
    const message = prompt('멘토에게 보낼 메시지를 입력하세요:')
    if (!message) return

    try {
      await axios.post('/match-requests', {
        mentorId,
        menteeId: user.id,
        message
      })
      alert('요청이 성공적으로 전송되었습니다!')
    } catch (error) {
      alert('요청 전송에 실패했습니다: ' + (error.response?.data?.detail || error.message))
    }
  }

  if (user?.role !== 'mentee') {
    return <Navigate to="/profile" />
  }

  return (
    <div className="container">
      <h2 className="mb-4 page-title">
        <span className="title-icon">🔍</span>
        멘토 찾기
      </h2>
      
      <div className="search-controls">
        <input
          id="search"
          type="text"
          placeholder="기술 스택으로 검색..."
          value={searchSkill}
          onChange={(e) => setSearchSkill(e.target.value)}
          className="form-input"
          style={{ flex: 1 }}
        />
        <select
          value={orderBy}
          onChange={(e) => setOrderBy(e.target.value)}
          className="form-select"
          style={{ width: '200px' }}
        >
          <option value="">기본 정렬</option>
          <option value="name">이름순</option>
          <option value="skill">기술스택순</option>
        </select>
        <button id="name" onClick={() => setOrderBy('name')} className="btn btn-secondary">
          이름순
        </button>
        <button id="skill" onClick={() => setOrderBy('skill')} className="btn btn-secondary">
          스킬순
        </button>
      </div>

      {loading ? (
        <div className="loading"><div className="spinner"></div></div>
      ) : (
        <div className="grid grid-3">
          {mentors.map((mentor) => (
            <div key={mentor.id} className="mentor-card mentor">
              <img
                src={mentor.profile.imageUrl}
                alt={mentor.profile.name}
                className="mentor-avatar"
              />
              <div className="mentor-name">{mentor.profile.name}</div>
              <div className="mentor-bio">{mentor.profile.bio}</div>
              <div className="skills">
                {mentor.profile.skills.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                ))}
              </div>
              <button
                id="request"
                onClick={() => sendRequest(mentor.id)}
                className="btn btn-primary"
                style={{ width: '100%' }}
              >
                매칭 요청
              </button>
              <input
                id="message"
                data-mentor-id={mentor.id}
                data-testid={`message-${mentor.id}`}
                type="hidden"
                value=""
              />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// Requests Component
const Requests = () => {
  const { user } = useAuth()
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRequests()
  }, [])

  const fetchRequests = async () => {
    try {
      const endpoint = user.role === 'mentor' ? '/match-requests/incoming' : '/match-requests/outgoing'
      const response = await axios.get(endpoint)
      setRequests(response.data)
    } catch (error) {
      console.error('Failed to fetch requests:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAccept = async (requestId) => {
    try {
      await axios.put(`/match-requests/${requestId}/accept`)
      fetchRequests()
      alert('요청을 수락했습니다!')
    } catch (error) {
      alert('요청 수락에 실패했습니다.')
    }
  }

  const handleReject = async (requestId) => {
    try {
      await axios.put(`/match-requests/${requestId}/reject`)
      fetchRequests()
      alert('요청을 거절했습니다.')
    } catch (error) {
      alert('요청 거절에 실패했습니다.')
    }
  }

  const handleCancel = async (requestId) => {
    try {
      await axios.delete(`/match-requests/${requestId}`)
      fetchRequests()
      alert('요청을 취소했습니다.')
    } catch (error) {
      alert('요청 취소에 실패했습니다.')
    }
  }

  const getStatusClass = (status) => {
    switch (status) {
      case 'pending': return 'status-pending'
      case 'accepted': return 'status-accepted'
      case 'rejected': return 'status-rejected'
      case 'cancelled': return 'status-cancelled'
      default: return ''
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'pending': return '대기중'
      case 'accepted': return '수락됨'
      case 'rejected': return '거절됨'
      case 'cancelled': return '취소됨'
      default: return status
    }
  }

  return (
    <div className="container">
      <h2 className="mb-4 page-title">
        <span className="title-icon">{user.role === 'mentor' ? '📥' : '📤'}</span>
        {user.role === 'mentor' ? '받은 매칭 요청' : '보낸 매칭 요청'}
      </h2>

      {loading ? (
        <div className="loading"><div className="spinner"></div></div>
      ) : (
        <div className="grid grid-2">
          {requests.map((request) => (
            <div key={request.id} className="card">
              <div className="mb-4">
                <span className={getStatusClass(request.status)} id="request-status">
                  {getStatusText(request.status)}
                </span>
              </div>
              
              {user.role === 'mentor' ? (
                <>
                  <div className="mb-4">
                    <strong>멘티 ID:</strong> {request.menteeId}
                  </div>
                  <div className="mb-4 request-message" mentee={request.menteeId}>
                    <strong>메시지:</strong> {request.message}
                  </div>
                  {request.status === 'pending' && (
                    <div style={{ display: 'flex', gap: '12px' }}>
                      <button
                        id="accept"
                        onClick={() => handleAccept(request.id)}
                        className="btn btn-success"
                      >
                        수락
                      </button>
                      <button
                        id="reject"
                        onClick={() => handleReject(request.id)}
                        className="btn btn-danger"
                      >
                        거절
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <>
                  <div className="mb-4">
                    <strong>멘토 ID:</strong> {request.mentorId}
                  </div>
                  {request.status === 'pending' && (
                    <button
                      onClick={() => handleCancel(request.id)}
                      className="btn btn-danger"
                    >
                      요청 취소
                    </button>
                  )}
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// 모바일 친화적 로딩 스피너
const LoadingSpinner = ({ message = "로딩 중..." }) => (
  <div className="loading-container">
    <div className="loading-spinner">
      <div className="spinner-ring"></div>
      <div className="spinner-ring"></div>
      <div className="spinner-ring"></div>
    </div>
    <p className="loading-message">{message}</p>
  </div>
)

// 터치 친화적 버튼 컴포넌트
const TouchButton = ({ children, className = '', onClick, disabled, ...props }) => (
  <button
    className={`btn touchable clickable ${className}`}
    onClick={onClick}
    disabled={disabled}
    {...props}
  >
    {children}
  </button>
)

// 모바일 친화적 카드 컴포넌트
const MobileCard = ({ children, className = '', onSwipeLeft, onSwipeRight, ...props }) => {
  const touchHandlers = useTouch(onSwipeLeft, onSwipeRight)
  
  return (
    <div
      className={`card touchable ${className}`}
      {...touchHandlers}
      {...props}
    >
      {children}
    </div>
  )
}

// 풀 스크린 모달 (모바일용)
const MobileModal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null

  return (
    <div className="mobile-modal-overlay" onClick={onClose}>
      <div className="mobile-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="mobile-modal-header">
          <h3>{title}</h3>
          <button className="mobile-modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        <div className="mobile-modal-body scrollable">
          {children}
        </div>
      </div>
    </div>
  )
}

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>
  }

  if (!user) {
    return <Navigate to="/login" />
  }

  return children
}

// Home Component
const Home = () => {
  const { user } = useAuth()
  const isMobileView = useResponsive()

  if (user) {
    return <Navigate to="/profile" />
  }

  return (
    <div className="container" style={{ marginTop: isMobileView ? '20px' : '50px' }}>
      <div className="text-center">
        <div style={{ 
          textAlign: 'center', 
          marginBottom: isMobileView ? '30px' : '50px',
          padding: isMobileView ? '24px 16px' : '40px 20px',
          background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
          borderRadius: isMobileView ? '12px' : '20px',
          boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)'
        }}>
          <h1 style={{ 
            fontSize: isMobileView ? '36px' : '64px', 
            marginBottom: isMobileView ? '12px' : '20px',
            fontWeight: 'bold',
            color: '#2d3748',
            textShadow: '2px 2px 4px rgba(0, 0, 0, 0.1)',
            lineHeight: '1.2'
          }}>
            🌅 RiseWith
          </h1>
          <p style={{ 
            fontSize: isMobileView ? '16px' : '24px', 
            color: '#4a5568', 
            marginBottom: '0',
            fontWeight: '500',
            letterSpacing: '0.5px',
            textShadow: '1px 1px 2px rgba(0, 0, 0, 0.05)'
          }}>
            함께 일어서고, 함께 성장하는 플랫폼
          </p>
          
          {/* 추가 설명 */}
          <div style={{
            marginTop: isMobileView ? '12px' : '20px',
            padding: isMobileView ? '12px' : '15px',
            background: 'rgba(102, 126, 234, 0.1)',
            borderRadius: isMobileView ? '8px' : '12px',
            border: '1px solid rgba(102, 126, 234, 0.2)'
          }}>
            <p style={{
              fontSize: isMobileView ? '14px' : '16px',
              color: '#2d3748',
              margin: '0',
              fontStyle: 'italic'
            }}>
              "Rise" 일어서다 + "With" 함께 = 동반성장의 여정
            </p>
          </div>
        </div>
        
        {/* 역할별 소개 */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: isMobileView ? '1fr' : '1fr 1fr', 
          gap: isMobileView ? '16px' : '30px', 
          maxWidth: '800px', 
          margin: isMobileView ? '0 auto 24px' : '0 auto 40px' 
        }}>
          <MobileCard style={{
            background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
            color: 'white',
            textAlign: 'center',
            padding: isMobileView ? '24px 20px' : '40px 30px',
            border: 'none',
            boxShadow: '0 15px 35px rgba(37, 99, 235, 0.3)',
            borderRadius: '16px'
          }}>
            <div style={{ fontSize: isMobileView ? '40px' : '56px', marginBottom: isMobileView ? '12px' : '20px', filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.3))' }}>🌅</div>
            <h3 style={{ 
              marginBottom: isMobileView ? '12px' : '20px', 
              color: 'white', 
              fontSize: isMobileView ? '20px' : '28px',
              fontWeight: 'bold',
              textShadow: '1px 1px 2px rgba(0, 0, 0, 0.3)'
            }}>Rise Mentor</h3>
            <p style={{ 
              fontSize: isMobileView ? '14px' : '18px', 
              lineHeight: '1.7', 
              opacity: 0.95,
              fontWeight: '400',
              textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)'
            }}>
              경험과 지식으로 다른 이들의<br/>
              <strong>성공적인 도약</strong>을 함께 이끌어주세요
            </p>
          </MobileCard>
          
          <MobileCard style={{
            background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
            color: 'white',
            textAlign: 'center',
            padding: isMobileView ? '24px 20px' : '40px 30px',
            border: 'none',
            boxShadow: '0 15px 35px rgba(5, 150, 105, 0.3)',
            borderRadius: '16px'
          }}>
            <div style={{ fontSize: isMobileView ? '40px' : '56px', marginBottom: isMobileView ? '12px' : '20px', filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.3))' }}>🤲</div>
            <h3 style={{ 
              marginBottom: isMobileView ? '12px' : '20px', 
              color: 'white', 
              fontSize: isMobileView ? '20px' : '28px',
              fontWeight: 'bold',
              textShadow: '1px 1px 2px rgba(0, 0, 0, 0.3)'
            }}>Rise Together</h3>
            <p style={{ 
              fontSize: isMobileView ? '14px' : '18px', 
              lineHeight: '1.7', 
              opacity: 0.95,
              fontWeight: '400',
              textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)'
            }}>
              멘토와 함께 손을 잡고<br/>
              <strong>더 높은 곳</strong>으로 함께 올라가세요
            </p>
          </MobileCard>
        </div>
        
        <div style={{ 
          display: 'flex', 
          flexDirection: isMobileView ? 'column' : 'row',
          gap: isMobileView ? '12px' : '20px', 
          justifyContent: 'center',
          alignItems: 'center',
          maxWidth: isMobileView ? '100%' : 'auto'
        }}>
          <TouchButton 
            className="btn-primary haptic-feedback" 
            style={{ 
              padding: isMobileView ? '16px 24px' : '18px 36px', 
              fontSize: isMobileView ? '16px' : '20px',
              fontWeight: 'bold',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              borderRadius: '12px',
              textShadow: '1px 1px 2px rgba(0, 0, 0, 0.2)',
              boxShadow: '0 8px 20px rgba(102, 126, 234, 0.3)',
              transform: 'translateY(0)',
              transition: 'all 0.3s ease',
              width: isMobileView ? '100%' : 'auto',
              textDecoration: 'none',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            onClick={() => window.location.href = '/login'}
          >
            🚀 시작하기
          </TouchButton>
          <TouchButton 
            className="btn-secondary haptic-feedback" 
            style={{ 
              padding: isMobileView ? '16px 24px' : '18px 36px', 
              fontSize: isMobileView ? '16px' : '20px',
              fontWeight: 'bold',
              borderRadius: '12px',
              boxShadow: '0 8px 20px rgba(0, 0, 0, 0.1)',
              transform: 'translateY(0)',
              transition: 'all 0.3s ease',
              width: isMobileView ? '100%' : 'auto',
              textDecoration: 'none',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
            onClick={() => window.location.href = '/signup'}
          >
            📝 회원가입
          </TouchButton>
        </div>
      </div>
    </div>
  )
}

// Theme wrapper component
const ThemedApp = () => {
  const { user } = useAuth()
  
  useEffect(() => {
    if (user) {
      document.body.className = `theme-${user.role}`
    } else {
      document.body.className = ''
    }
    
    return () => {
      document.body.className = ''
    }
  }, [user])
  
  return (
    <div className={`App ${user ? `theme-${user.role}` : ''}`}>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/profile" element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } />
        <Route path="/mentors" element={
          <ProtectedRoute>
            <Mentors />
          </ProtectedRoute>
        } />
        <Route path="/requests" element={
          <ProtectedRoute>
            <Requests />
          </ProtectedRoute>
        } />
      </Routes>
    </div>
  )
}

// Main App Component
function App() {
  return (
    <AuthProvider>
      <Router>
        <ThemedApp />
      </Router>
    </AuthProvider>
  )
}

export default App
