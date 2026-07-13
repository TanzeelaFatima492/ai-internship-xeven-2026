'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { AlertCircle, Eye, EyeOff, Loader2, CheckCircle2 } from 'lucide-react'

interface SignupFormProps {
  loading: boolean
  setLoading: (loading: boolean) => void
}

export default function SignupForm({ loading, setLoading }: SignupFormProps) {
  const router = useRouter()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateEmail = (email: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setIsSubmitting(true)

    // Client-side validation
    if (!username.trim()) {
      setError('Username is required')
      setIsSubmitting(false)
      return
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid email address')
      setIsSubmitting(false)
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      setIsSubmitting(false)
      return
    }

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.error || 'Signup failed')
        return
      }

      // Store JWT token
      localStorage.setItem('token', data.token)

      setSuccess('Account created successfully!')
      setTimeout(() => {
        router.push('/home')
      }, 1500)
    } catch (err) {
      setError('Something went wrong. Please try again.')
      console.error(err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Username Field */}
      <div className="space-y-2">
        <label htmlFor="signup-username" className="block text-sm font-medium text-foreground">
          Username
        </label>
        <input
          id="signup-username"
          type="text"
          placeholder="Choose a username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-4 py-3 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
          disabled={isSubmitting}
        />
      </div>

      {/* Email Field */}
      <div className="space-y-2">
        <label htmlFor="signup-email" className="block text-sm font-medium text-foreground">
          Email
        </label>
        <input
          id="signup-email"
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-3 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
          disabled={isSubmitting}
        />
      </div>

      {/* Password Field */}
      <div className="space-y-2">
        <label htmlFor="signup-password" className="block text-sm font-medium text-foreground">
          Password
        </label>
        <div className="relative">
          <input
            id="signup-password"
            type={showPassword ? 'text' : 'password'}
            placeholder="Create a password (min. 6 chars)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200 pr-10"
            disabled={isSubmitting}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            tabIndex={-1}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="flex items-center gap-3 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
          <AlertCircle size={18} className="text-destructive flex-shrink-0" />
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="flex items-center gap-3 p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
          <CheckCircle2 size={18} className="text-green-500 flex-shrink-0" />
          <p className="text-sm text-green-500">{success}</p>
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting || !username.trim() || !email.trim() || !password.trim()}
        className="w-full py-3 px-4 bg-gradient-to-r from-primary via-accent to-secondary text-primary-foreground font-semibold rounded-lg transition-all duration-200 hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-6"
      >
        {isSubmitting ? (
          <>
            <Loader2 size={18} className="animate-spin" />
            Creating account...
          </>
        ) : (
          'Sign Up'
        )}
      </button>

      {/* Help text */}
      <p className="text-xs text-center text-muted-foreground mt-4">
        Join our AI-powered food assistant platform
      </p>
    </form>
  )
}
