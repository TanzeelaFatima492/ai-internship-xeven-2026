'use client'

import { useState } from 'react'
import { AlertCircle, Loader2, ChefHat, Eye, EyeOff } from 'lucide-react'

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [role, setRole] = useState('customer')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    
    if (!username.trim()) { setError('Username is required'); return }
    if (!password.trim()) { setError('Password is required'); return }
    
    setLoading(true)

    const url = isLogin 
      ? 'http://localhost:8000/auth/login'
      : 'http://localhost:8000/auth/signup'

    const body = isLogin 
      ? JSON.stringify({ username, password })
      : JSON.stringify({ username, email, password })

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Invalid credentials')
        setLoading(false)
        return
      }

      if (isLogin) {
        localStorage.setItem('bitewise_auth_token', data.access_token)
        localStorage.setItem('user_role', data.role)
        window.location.href = data.role === 'admin' ? '/admin' : '/home'
      } else {
        setSuccess('Account created! Please login.')
        setIsLogin(true)
        setPassword('')
        setLoading(false)
      }
    } catch {
      setError('Backend not running. Start backend on port 8000.')
      setLoading(false)
    }
  }

  const inputClass = "w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none"

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-50 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-6">
          <div className="inline-block bg-gradient-to-br from-orange-500 to-orange-600 p-4 rounded-2xl shadow-lg mb-3">
            <ChefHat className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">BiteWise</h1>
          <p className="text-gray-500 text-sm">AI Food Assistant</p>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-xl p-6">
          <div className="flex border-b border-gray-200 mb-5">
            <button type="button" onClick={() => { setIsLogin(true); setError(''); setSuccess('') }}
              className={`flex-1 pb-3 font-semibold text-sm ${isLogin ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-400'}`}>
              Login
            </button>
            <button type="button" onClick={() => { setIsLogin(false); setError(''); setSuccess('') }}
              className={`flex-1 pb-3 font-semibold text-sm ${!isLogin ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-400'}`}>
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username *</label>
              <input type="text" placeholder="Enter username" value={username}
                onChange={e => setUsername(e.target.value)} className={inputClass} />
            </div>

            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input type="email" placeholder="Enter email" value={email}
                  onChange={e => setEmail(e.target.value)} className={inputClass} />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password *</label>
              <div className="relative">
                <input type={showPassword ? 'text' : 'password'} placeholder="Enter password" value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none pr-10" />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700">
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Login as</label>
                <select value={role} onChange={e => setRole(e.target.value)} className={inputClass}>
                  <option value="customer">Customer</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
            )}

            {error && (
              <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <AlertCircle size={16} className="text-red-500 flex-shrink-0" />
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            {success && (
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-600">{success}</p>
              </div>
            )}

            <button type="submit" disabled={loading}
              className="w-full py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2">
              {loading && <Loader2 size={18} className="animate-spin" />}
              {isLogin ? 'Login' : 'Sign Up'}
            </button>
          </form>
        </div>

        <p className="text-center text-gray-400 text-xs mt-4">
          Admin: admin / admin123
        </p>
      </div>
    </main>
  )
}