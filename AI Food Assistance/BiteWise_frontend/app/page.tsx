'use client'

import { useState } from 'react'
import { AlertCircle, Loader2, ChefHat } from 'lucide-react'

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
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
        // Auto-redirect based on role from backend
        window.location.href = data.role === 'admin' ? '/admin' : '/home'
      } else {
        setSuccess('Account created! You can now login.')
        setIsLogin(true)
        setPassword('')
        setLoading(false)
      }
    } catch {
      setError('Backend not running. Start backend on port 8000.')
      setLoading(false)
    }
  }

  const inputClass = "w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-100 outline-none transition-all duration-200"

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-50 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        {/* Logo + Brand Name in One Line */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-2.5 rounded-xl shadow-lg">
            <ChefHat className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">BiteWise</h1>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-xl p-6">
          {/* Tabs */}
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input type="password" placeholder="Enter password" value={password}
                onChange={e => setPassword(e.target.value)} className={inputClass} />
            </div>

            {error && (
              <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <AlertCircle size={16} className="text-red-500" />
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
          🍽️ Delicious Food, Smartly Delivered
        </p>
      </div>
    </main>
  )
}