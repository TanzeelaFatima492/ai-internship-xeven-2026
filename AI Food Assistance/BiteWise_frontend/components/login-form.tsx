'use client'

import { useState } from 'react'
import { AlertCircle, Eye, EyeOff, Loader2 } from 'lucide-react'

export default function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || 'Invalid credentials')
        return
      }

      // Store token and role
      localStorage.setItem('bitewise_auth_token', data.access_token)
      localStorage.setItem('user_role', data.role)

      // Force redirect based on role
      if (data.role === 'admin') {
        window.location.href = '/admin'
      } else {
        window.location.href = '/home'
      }
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
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-3 bg-background border border-border rounded-lg"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-2">
        <label className="block text-sm font-medium">Password</label>
        <div className="relative">
          <input
            type={showPassword ? 'text' : 'password'}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 bg-background border border-border rounded-lg pr-10"
            disabled={isSubmitting}
          />
          <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2">
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-3 bg-red-100 border border-red-200 rounded-lg">
          <AlertCircle size={18} className="text-red-500" />
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting || !username.trim() || !password.trim()}
        className="w-full py-3 px-4 bg-gradient-to-r from-orange-500 to-red-500 text-white font-semibold rounded-lg disabled:opacity-50"
      >
        {isSubmitting ? <Loader2 size={18} className="animate-spin inline" /> : 'Login'}
      </button>

      <p className="text-xs text-center text-gray-500 mt-4">
        Admin: admin / admin123 | Customer: Sign up first
      </p>
    </form>
  )
}