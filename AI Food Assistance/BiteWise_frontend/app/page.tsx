'use client'

import { useState } from 'react'
import { User, Mail, Lock, Eye, EyeOff } from 'lucide-react'

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [remember, setRemember] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setError(''); setSuccess('')
    if (!username.trim() || !password.trim()) { setError('Please fill all fields'); return }
    setLoading(true)
    const url = isLogin ? 'http://localhost:8000/auth/login' : 'http://localhost:8000/auth/signup'
    const body = isLogin ? JSON.stringify({ username, password }) : JSON.stringify({ username, email, password })
    try {
      const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body })
      const data = await res.json()
      if (!res.ok) { setError(data.detail || 'Error'); setLoading(false); return }
      if (isLogin) {
        localStorage.setItem('bitewise_auth_token', data.access_token)
        localStorage.setItem('user_role', data.role)
        window.location.replace(data.role === 'admin' ? '/admin' : '/home')
      } else {
        setSuccess('Account created! Login now.')
        setUsername(''); setEmail(''); setPassword(''); setIsLogin(true); setLoading(false)
      }
    } catch { setError('Server not reachable'); setLoading(false) }
  }

  const inputStyle: React.CSSProperties = {
    width:'100%', height:50, borderRadius:25, border:'none', background:'#F5F5F5',
    paddingLeft:50, fontSize:15, outline:'none', boxSizing:'border-box'
  }

  return (
    <div style={{minHeight:'100vh', display:'flex', background:'#ffffff', fontFamily:"'Inter', sans-serif"}}>
      {/* LEFT PANEL */}
      <div style={{
        width:'45%', background:'linear-gradient(180deg,#FFB25B,#FF8D5C)',
        borderTopRightRadius:320, borderBottomRightRadius:320,
        display:'flex', flexDirection:'column', justifyContent:'center', paddingLeft:80, color:'#fff'
      }}>
        <div style={{display:'flex', alignItems:'center', gap:12, marginBottom:30}}>
          <div style={{width:42, height:42, borderRadius:'50%', background:'rgba(255,255,255,.25)', display:'flex', justifyContent:'center', alignItems:'center', fontSize:20}}>🌸</div>
          <h2 style={{margin:0, fontSize:28, fontWeight:700}}>BiteWise</h2>
        </div>
        <h1 style={{fontSize:50, lineHeight:1.25, fontWeight:700, margin:0}}>Welcome to the<br />BiteWise<br />Community!</h1>
        <p style={{marginTop:20, fontSize:18, opacity:.95}}>Smart Restaurant Assistant</p>
      </div>

      {/* RIGHT PANEL */}
      <div style={{width:'55%', display:'flex', justifyContent:'center', alignItems:'center'}}>
        <div style={{width:420}}>
          {/* Profile Icon */}
          <div style={{width:90, height:90, borderRadius:'50%', background:'#EFEAFB', margin:'0 auto 25px', display:'flex', alignItems:'center', justifyContent:'center'}}>
            <User size={42} color="#AAA4C8" />
          </div>

          <p style={{color:'#777', marginBottom:30, fontSize:15, textAlign:'center'}}>
            {isLogin ? 'Login below to get started.' : 'Create your account.'}
          </p>

          {/* Username */}
          <div style={{position:'relative', marginBottom:18}}>
            <User size={18} style={{position:'absolute', left:18, top:'50%', transform:'translateY(-50%)', color:'#BDBDBD'}} />
            <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} style={inputStyle} />
          </div>

          {/* Email */}
          {!isLogin && (
            <div style={{position:'relative', marginBottom:18}}>
              <Mail size={18} style={{position:'absolute', left:18, top:'50%', transform:'translateY(-50%)', color:'#BDBDBD'}} />
              <input type="email" placeholder="E-mail Address" value={email} onChange={e => setEmail(e.target.value)} style={inputStyle} />
            </div>
          )}

          {/* Password */}
          <div style={{position:'relative', marginBottom:20}}>
            <Lock size={18} style={{position:'absolute', left:18, top:'50%', transform:'translateY(-50%)', color:'#BDBDBD'}} />
            <input type={showPassword ? 'text' : 'password'} placeholder="Your Password" value={password}
              onChange={e => setPassword(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') handleSubmit() }}
              style={{...inputStyle, paddingRight:50}} />
            <button type="button" onClick={() => setShowPassword(!showPassword)}
              style={{position:'absolute', right:15, top:'50%', transform:'translateY(-50%)', border:'none', background:'transparent', cursor:'pointer', color:'#999'}}>
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>

          {/* Remember */}
          {isLogin && (
            <div style={{display:'flex', alignItems:'center', gap:8, marginBottom:20}}>
              <input id="remember" type="checkbox" checked={remember} onChange={e => setRemember(e.target.checked)} />
              <label htmlFor="remember" style={{color:'#777', fontSize:14}}>Keep me logged in</label>
            </div>
          )}

          {error && <div style={{color:'#E53935', marginBottom:15, textAlign:'center'}}>{error}</div>}
          {success && <div style={{color:'#2E7D32', marginBottom:15, textAlign:'center'}}>{success}</div>}

          {/* Button */}
          <button onClick={handleSubmit} disabled={loading}
            style={{width:'100%', height:58, border:'none', borderRadius:35, background:'linear-gradient(90deg,#FF6A63,#FFB45C)', color:'#fff', fontWeight:700, fontSize:17, cursor:'pointer', boxShadow:'0 10px 25px rgba(255,120,90,.35)', opacity:loading?0.8:1}}>
            {loading ? 'Please wait...' : isLogin ? 'Login' : 'Create Account'}
          </button>

          {/* Footer */}
          <p style={{marginTop:30, fontSize:14, color:'#666', textAlign:'center'}}>
            {isLogin ? (
              <>New User? <a href="#" onClick={e => { e.preventDefault(); setIsLogin(false); setError(''); setSuccess('') }} style={{color:'#FF7A5B', fontWeight:600, textDecoration:'none'}}>Register here.</a></>
            ) : (
              <>Already have account? <a href="#" onClick={e => { e.preventDefault(); setIsLogin(true); setError(''); setSuccess('') }} style={{color:'#FF7A5B', fontWeight:600, textDecoration:'none'}}>Login</a></>
            )}
          </p>
        </div>
      </div>
    </div>
  )
}