"use client"

import type React from "react"
import { useState } from "react"
import { AlertCircle, Loader2, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { login, signup, type StoredUser } from "@/lib/api"

type Mode = "login" | "signup"

export function AuthView({
  onAuthenticated,
}: {
  onAuthenticated: (user: StoredUser | null) => void
}) {
  const [mode, setMode] = useState<Mode>("login")
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  const isSignup = mode === "signup"

  function switchMode(next: Mode) {
    setMode(next)
    setError(null)
    setNotice(null)
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setNotice(null)
    setLoading(true)

    try {
      if (isSignup) {
        await signup({ full_name: fullName, email, password })
        // Try to log in immediately after signup.
        try {
          const { user } = await login({ email, password })
          onAuthenticated(user)
        } catch {
          setNotice("Account created. Please log in.")
          switchMode("login")
        }
      } else {
        const { user } = await login({ email, password })
        onAuthenticated(user)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-dvh flex-col bg-background">
      <header className="flex items-center justify-between px-4 py-4 sm:px-6">
        <div className="flex items-center gap-2">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <MessageSquare className="size-4" />
          </div>
          <span className="font-heading text-lg font-semibold">Pulse Chat</span>
        </div>
        <ThemeToggle />
      </header>

      <main className="flex flex-1 items-center justify-center px-4 py-8">
        <div className="w-full max-w-sm">
          <div className="mb-8 text-center">
            <h1 className="text-balance font-heading text-2xl font-semibold tracking-tight">
              {isSignup ? "Create your account" : "Welcome back"}
            </h1>
            <p className="mt-2 text-pretty text-sm leading-relaxed text-muted-foreground">
              {isSignup
                ? "Sign up to start chatting."
                : "Log in to continue your conversations."}
            </p>
          </div>

          <div className="mb-6 grid grid-cols-2 gap-1 rounded-lg bg-muted p-1">
            <button
              type="button"
              onClick={() => switchMode("login")}
              className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                !isSignup
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Log in
            </button>
            <button
              type="button"
              onClick={() => switchMode("signup")}
              className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                isSignup
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Sign up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {isSignup && (
              <Field
                id="fullName"
                label="Full name"
                type="text"
                value={fullName}
                onChange={setFullName}
                placeholder="Jane Doe"
                autoComplete="name"
                required
              />
            )}
            <Field
              id="email"
              label="Email"
              type="email"
              value={email}
              onChange={setEmail}
              placeholder="you@example.com"
              autoComplete="email"
              required
            />
            <Field
              id="password"
              label="Password"
              type="password"
              value={password}
              onChange={setPassword}
              placeholder="••••••••"
              autoComplete={isSignup ? "new-password" : "current-password"}
              required
            />

            {error && (
              <div
                role="alert"
                className="flex items-start gap-2 rounded-lg bg-destructive/10 px-3 py-2 text-sm text-destructive"
              >
                <AlertCircle className="mt-0.5 size-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}
            {notice && (
              <div className="rounded-lg bg-primary/10 px-3 py-2 text-sm text-primary">
                {notice}
              </div>
            )}

            <Button
              type="submit"
              disabled={loading}
              size="lg"
              className="mt-2 h-11 w-full text-sm"
            >
              {loading && <Loader2 className="size-4 animate-spin" />}
              {isSignup ? "Create account" : "Log in"}
            </Button>
          </form>
        </div>
      </main>
    </div>
  )
}

function Field({
  id,
  label,
  type,
  value,
  onChange,
  placeholder,
  autoComplete,
  required,
}: {
  id: string
  label: string
  type: string
  value: string
  onChange: (v: string) => void
  placeholder?: string
  autoComplete?: string
  required?: boolean
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-medium">
        {label}
      </label>
      <input
        id={id}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        autoComplete={autoComplete}
        required={required}
        className="h-11 rounded-lg border border-input bg-background px-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
      />
    </div>
  )
}
