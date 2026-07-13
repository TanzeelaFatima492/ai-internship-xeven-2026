'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, Plus, MessageSquare } from 'lucide-react'
import ChatWindow from '@/components/chat-window'
import ChatSidebar from '@/components/chat-sidebar'

interface Thread {
  id: string
  title: string
  createdAt: Date
  preview: string
}

export default function HomePage() {
  const router = useRouter()
  const [user, setUser] = useState<{ username: string; email: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    // Get user info from token
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/')
      return
    }

    try {
      // Decode JWT token
      const payload = JSON.parse(
        Buffer.from(token.split('.')[1], 'base64').toString()
      )
      setUser({
        username: payload.username,
        email: payload.email,
      })
    } catch (err) {
      console.error('Invalid token:', err)
      localStorage.removeItem('token')
      router.push('/')
    } finally {
      setLoading(false)
    }

    // Load threads from localStorage
    const savedThreads = localStorage.getItem('chatThreads')
    if (savedThreads) {
      try {
        setThreads(JSON.parse(savedThreads))
      } catch (err) {
        console.error('Error loading threads:', err)
      }
    }
  }, [router])

  const handleNewChat = () => {
    setActiveThreadId(null)
  }

  const handleSelectThread = (threadId: string) => {
    setActiveThreadId(threadId)
  }

  const handleSaveThread = (thread: Thread) => {
    const existing = threads.find(t => t.id === thread.id)
    let updatedThreads

    if (existing) {
      updatedThreads = threads.map(t => t.id === thread.id ? thread : t)
    } else {
      updatedThreads = [thread, ...threads]
    }

    setThreads(updatedThreads)
    localStorage.setItem('chatThreads', JSON.stringify(updatedThreads))
    setActiveThreadId(thread.id)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-background/95 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <main className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-primary via-accent to-secondary p-2 rounded-lg">
              <ChefHat className="w-6 h-6 text-card" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">BiteWise</h1>
              <p className="text-xs text-muted-foreground">Restaurant AI Assistant</p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 md:px-4 py-2 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg transition-colors text-sm md:text-base"
          >
            <LogOut size={18} />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>

      {/* Main Chat Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Hidden on mobile by default */}
        <ChatSidebar
          threads={threads}
          activeThreadId={activeThreadId}
          onSelectThread={handleSelectThread}
          onNewChat={handleNewChat}
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        {/* Chat Window */}
        <ChatWindow
          user={user}
          activeThreadId={activeThreadId}
          onSaveThread={handleSaveThread}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />
      </div>
    </main>
  )
}
