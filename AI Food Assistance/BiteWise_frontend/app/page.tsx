'use client'

import { useState } from 'react'
import { AlertCircle, CheckCircle2, Loader2, ChefHat, Eye, EyeOff } from 'lucide-react'

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState<{username?: string; email?: string; password?: string}>({})
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const validate = (): boolean => {
    const errors: {username?: string; email?: string; password?: string} = {}
    if (!username.trim()) errors.username = 'Username is required'
    else if (username.length < 3) errors.username = 'Username must be at least 3 characters'
    if (!isLogin && !email.trim()) errors.email = 'Email is required'
    else if (!isLogin && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = 'Enter a valid email'
    if (!password.trim()) errors.password = 'Password is required'
    else if (password.length < 6) errors.password = 'Password must be at least 6 characters'
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    if (!validate()) return
    setLoading(true)

    const url = isLogin ? 'http://localhost:8000/auth/login' : 'http://localhost:8000/auth/signup'
    const body = isLogin ? JSON.stringify({ username, password }) : JSON.stringify({ username, email, password })

    try {
      const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body })
      const data = await res.json()

      if (!res.ok) {
        const msg = data.detail || 'Something went wrong'
        if (msg.toLowerCase().includes('already exists')) setError('⚠️ This email is already registered. Please login instead.')
        else if (msg.toLowerCase().includes('invalid')) setError('❌ Invalid username or password.')
        else setError(msg)
        setLoading(false)
        return
      }

      if (isLogin) {
        localStorage.setItem('bitewise_auth_token', data.access_token)
        localStorage.setItem('user_role', data.role)
        window.location.href = data.role === 'admin' ? '/admin' : '/home'
      } else {
        setSuccess('✅ Account created successfully! You can now login.')
        setIsLogin(true)
        setUsername('')
        setEmail('')
        setPassword('')
        setFieldErrors({})
        setLoading(false)
      }
    } catch {
      setError('🔌 Cannot connect to server. Is backend running on port 8000?')
      setLoading(false)
    }
  }

  const switchTab = (login: boolean) => {
    setIsLogin(login)
    setError('')
    setSuccess('')
    setFieldErrors({})
    setPassword('')
  }

  const inputClass = "w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:border-orange-500 focus:ring-2 focus:ring-orange-100 outline-none transition-all duration-200"
  const errorInputClass = "w-full px-4 py-3 border-2 border-red-300 rounded-xl text-gray-900 placeholder-gray-400 focus:border-red-500 focus:ring-2 focus:ring-red-100 outline-none bg-red-50"

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-orange-50 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-2.5 rounded-xl shadow-lg">
            <ChefHat className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">BiteWise</h1>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-xl p-6">
          <div className="flex border-b border-gray-200 mb-5">
            <button type="button" onClick={() => switchTab(true)} className={`flex-1 pb-3 font-semibold text-sm ${isLogin ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-400'}`}>Login</button>
            <button type="button" onClick={() => switchTab(false)} className={`flex-1 pb-3 font-semibold text-sm ${!isLogin ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-400'}`}>Sign Up</button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4" noValidate>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username <span className="text-red-500">*</span></label>
              <input type="text" placeholder="Enter username" value={username} onChange={e => { setUsername(e.target.value); setFieldErrors(p => ({...p, username: undefined})) }} className={fieldErrors.username ? errorInputClass : inputClass} />
              {fieldErrors.username && <p className="text-red-500 text-xs mt-1 flex items-center gap-1"><AlertCircle size={12} />{fieldErrors.username}</p>}
            </div>

            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email <span className="text-red-500">*</span></label>
                <input type="email" placeholder="Enter email" value={email} onChange={e => { setEmail(e.target.value); setFieldErrors(p => ({...p, email: undefined})) }} className={fieldErrors.email ? errorInputClass : inputClass} />
                {fieldErrors.email && <p className="text-red-500 text-xs mt-1 flex items-center gap-1"><AlertCircle size={12} />{fieldErrors.email}</p>}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password <span className="text-red-500">*</span></label>
              <div className="relative">
                <input type={showPassword ? 'text' : 'password'} placeholder="Enter password" value={password} onChange={e => { setPassword(e.target.value); setFieldErrors(p => ({...p, password: undefined})) }} className={`${fieldErrors.password ? errorInputClass : inputClass} pr-10`} />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button>
              </div>
              {fieldErrors.password && <p className="text-red-500 text-xs mt-1 flex items-center gap-1"><AlertCircle size={12} />{fieldErrors.password}</p>}
            </div>

            {error && <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg"><AlertCircle size={16} className="text-red-500 flex-shrink-0" /><p className="text-sm text-red-600">{error}</p></div>}
            {success && <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg"><CheckCircle2 size={16} className="text-green-500 flex-shrink-0" /><p className="text-sm text-green-600">{success}</p></div>}

            <button type="submit" disabled={loading} className="w-full py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-md">
              {loading && <Loader2 size={18} className="animate-spin" />}
              {loading ? 'Please wait...' : isLogin ? 'Login' : 'Sign Up'}
            </button>
          </form>
        </div>

        <p className="text-center text-gray-400 text-xs mt-4">🍽️ Delicious Food, Smartly Delivered</p>
      </div>
    </main>
  )
}