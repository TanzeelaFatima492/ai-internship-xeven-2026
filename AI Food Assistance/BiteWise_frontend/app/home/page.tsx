'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, MessageSquare } from 'lucide-react'
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
  const [user, setUser] = useState<{ username: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    const role = localStorage.getItem('user_role')
    if (!token) { router.push('/'); return }
    if (role === 'admin') { router.push('/admin'); return }
    
    setUser({ username: 'Customer' })

    // Fetch real threads from backend
    fetch('http://localhost:8000/rag/threads', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => {
      if (Array.isArray(data)) {
        setThreads(data.map((t: any) => ({
          id: t.thread_id,
          title: t.thread_id,
          createdAt: new Date(),
          preview: '',
        })))
      }
    })
    .catch(console.error)
    .finally(() => setLoading(false))
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('bitewise_auth_token')
    localStorage.removeItem('user_role')
    router.push('/')
  }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="animate-spin h-12 w-12 border-b-2 border-orange-500 rounded-full"></div>
    </div>
  )

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 p-2 rounded-lg">
            <ChefHat className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">BiteWise</h1>
            <p className="text-xs text-gray-500">Restaurant AI Assistant</p>
          </div>
        </div>
        <button onClick={handleLogout} className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg">
          <LogOut size={18} /> Logout
        </button>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <ChatSidebar
          threads={threads}
          activeThreadId={activeThreadId}
          onSelectThread={setActiveThreadId}
          onNewChat={() => setActiveThreadId(null)}
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />
        <ChatWindow
          user={user}
          activeThreadId={activeThreadId}
          onSaveThread={(thread) => {
            setThreads(prev => [thread, ...prev])
          }}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />
      </div>
    </main>
  )
}