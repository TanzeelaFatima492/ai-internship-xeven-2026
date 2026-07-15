"use client"

import { useEffect, useState } from "react"
import { AuthView } from "@/components/auth-view"
import { ChatView } from "@/components/chat-view"
import {
  clearAuth,
  getStoredUser,
  getToken,
  type StoredUser,
} from "@/lib/api"

export default function Page() {
  const [ready, setReady] = useState(false)
  const [authed, setAuthed] = useState(false)
  const [user, setUser] = useState<StoredUser | null>(null)

  useEffect(() => {
    const token = getToken()
    if (token) {
      setUser(getStoredUser())
      setAuthed(true)
    }
    setReady(true)
  }, [])

  function handleAuthenticated(u: StoredUser | null) {
    setUser(u)
    setAuthed(true)
  }

  function handleLogout() {
    clearAuth()
    setUser(null)
    setAuthed(false)
  }

  if (!ready) {
    return (
      <div className="flex h-dvh items-center justify-center bg-background">
        <div className="size-6 animate-spin rounded-full border-2 border-muted border-t-primary" />
      </div>
    )
  }

  if (!authed) {
    return <AuthView onAuthenticated={handleAuthenticated} />
  }

  return <ChatView user={user} onLogout={handleLogout} />
}
