'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { AlertCircle, Eye, EyeOff, Loader2, CheckCircle2 } from 'lucide-react'

export default function SignupForm() {
  const router = useRouter()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setIsSubmitting(true)

    if (!username.trim()) { setError('Username is required'); setIsSubmitting(false); return }
    if (password.length < 6) { setError('Password must be at least 6 characters'); setIsSubmitting(false); return }

    try {
      const response = await fetch('http://localhost:8000/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || 'Signup failed')
        return
      }

      setSuccess('Account created! Redirecting to login...')
      setTimeout(() => {
        router.push('/')
      }, 1500)
    } catch (err) {
      setError('Something went wrong. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <label className="block text-sm font-medium">Username</label>
        <input type="text" placeholder="Choose a username" value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg" disabled={isSubmitting} />
      </div>

      <div className="space-y-2">
        <label className="block text-sm font-medium">Email</label>
        <input type="email" placeholder="Enter your email" value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg" disabled={isSubmitting} />
      </div>

      <div className="space-y-2">
        <label className="block text-sm font-medium">Password</label>
        <div className="relative">
          <input type={showPassword ? 'text' : 'password'} placeholder="Min. 6 characters" value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg pr-10" disabled={isSubmitting} />
          <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2">
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-3 bg-red-50 border border-red-200 rounded-lg">
          <AlertCircle size={18} className="text-red-500" />
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {success && (
        <div className="flex items-center gap-3 p-3 bg-green-50 border border-green-200 rounded-lg">
          <CheckCircle2 size={18} className="text-green-500" />
          <p className="text-sm text-green-600">{success}</p>
        </div>
      )}

      <button type="submit" disabled={isSubmitting || !username.trim() || !password.trim()}
        className="w-full py-3 px-4 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-semibold rounded-lg disabled:opacity-50">
        {isSubmitting ? <Loader2 size={18} className="animate-spin inline" /> : 'Sign Up'}
      </button>

      <p className="text-xs text-center text-gray-500 mt-4">Join our AI-powered food assistant platform</p>
    </form>
  )
}