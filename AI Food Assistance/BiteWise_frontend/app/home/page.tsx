'use client'

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, Plus, MessageSquare, Send, Loader2, FileText } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  source?: string
  timestamp: Date
}

interface Thread {
  id: string
  title: string
  createdAt: Date
}

export default function HomePage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    const role = localStorage.getItem('user_role')
    if (!token) { router.push('/'); return }
    if (role === 'admin') { router.push('/admin'); return }

    fetch('http://localhost:8000/rag/threads', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => {
      if (Array.isArray(data)) {
        setThreads(data.map((t: any) => ({ id: t.thread_id, title: t.thread_id, createdAt: new Date() })))
      }
    })
    .catch(console.error)
    .finally(() => setLoading(false))
  }, [router])

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  const handleSend = async () => {
    if (!input.trim() || sending) return
    const token = localStorage.getItem('bitewise_auth_token')
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input, timestamp: new Date() }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setSending(true)

    try {
      const res = await fetch('http://localhost:8000/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ question: userMsg.content, top_k: 3, conversation_id: activeThreadId || undefined }),
      })
      const data = await res.json()
      const aiMsg: Message = { id: (Date.now() + 1).toString(), role: 'ai', content: data.answer, source: data.sources?.[0]?.document_name, timestamp: new Date() }
      setMessages(prev => [...prev, aiMsg])
      if (!activeThreadId) {
        const newThread = { id: `thread-${Date.now()}`, title: userMsg.content.substring(0, 40), createdAt: new Date() }
        setActiveThreadId(newThread.id)
        setThreads(prev => [newThread, ...prev])
      }
    } catch { /* error */ }
    finally { setSending(false) }
  }

  const handleNewChat = () => { setActiveThreadId(null); setMessages([]) }

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50"><div className="animate-spin h-10 w-10 border-b-2 border-orange-500 rounded-full"></div></div>

  return (
    <div className="h-screen flex bg-gray-50">
      {/* SIDEBAR - Fixed, independent scroll */}
      <div className="w-72 bg-white border-r border-gray-200 flex flex-col flex-shrink-0">
        <div className="p-5 border-b border-gray-100">
          <div className="flex items-center gap-2 mb-4">
            <div className="bg-orange-500 p-1.5 rounded-lg"><ChefHat className="w-5 h-5 text-white" /></div>
            <span className="font-bold text-gray-800 text-lg">BiteWise</span>
          </div>
          <button onClick={handleNewChat} className="w-full flex items-center gap-2 px-4 py-2.5 bg-orange-500 text-white rounded-xl hover:bg-orange-600 transition-all font-medium text-sm">
            <Plus size={18} /> New Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          {threads.map(t => (
            <button key={t.id} onClick={() => setActiveThreadId(t.id)}
              className={`w-full text-left px-3 py-2.5 rounded-xl text-sm transition-all truncate ${activeThreadId === t.id ? 'bg-orange-50 text-orange-700 font-medium' : 'text-gray-600 hover:bg-gray-50'}`}>
              <MessageSquare size={14} className="inline mr-2 opacity-50" />{t.title}
            </button>
          ))}
        </div>
        <div className="p-4 border-t border-gray-100">
          <button onClick={() => { localStorage.clear(); router.push('/') }} className="flex items-center gap-2 text-sm text-gray-500 hover:text-red-500 w-full">
            <LogOut size={16} /> Logout
          </button>
        </div>
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-3 flex-shrink-0">
          <div className="bg-orange-100 p-2 rounded-lg"><ChefHat className="w-5 h-5 text-orange-600" /></div>
          <div>
            <h1 className="font-semibold text-gray-900">{activeThreadId ? 'Conversation' : 'New Chat'}</h1>
            <p className="text-xs text-gray-400">Ask about menu, prices & offers</p>
          </div>
        </header>

        {/* Messages - Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center">
              <div className="bg-orange-100 p-6 rounded-full mb-4"><ChefHat className="w-12 h-12 text-orange-500" /></div>
              <h2 className="text-xl font-bold text-gray-800 mb-2">Welcome to BiteWise! 🍽️</h2>
              <p className="text-gray-400 max-w-sm">Ask me about our authentic Pakistani menu, prices, special offers, or restaurant policies.</p>
            </div>
          ) : (
            messages.map(m => (
              <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] px-5 py-3 rounded-2xl ${m.role === 'user' ? 'bg-orange-500 text-white rounded-br-md' : 'bg-white border border-gray-200 text-gray-800 rounded-bl-md shadow-sm'}`}>
                  <p className="text-sm leading-relaxed">{m.content}</p>
                  {m.source && <div className="flex items-center gap-1 mt-2 pt-2 border-t border-gray-100 text-xs text-gray-400"><FileText size={12} />{m.source}</div>}
                </div>
              </div>
            ))
          )}
          {sending && <div className="flex justify-start"><div className="bg-white border px-5 py-3 rounded-2xl rounded-bl-md shadow-sm"><Loader2 className="w-4 h-4 text-orange-500 animate-spin" /></div></div>}
          <div ref={messagesEndRef} />
        </div>

        {/* Input - Fixed bottom */}
        <div className="bg-white border-t border-gray-200 px-6 py-4 flex-shrink-0">
          <div className="flex items-center gap-3 max-w-3xl mx-auto">
            <input type="text" value={input} onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() } }}
              placeholder="Ask about menu, prices, or anything else..." disabled={sending}
              className="flex-1 px-5 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-orange-200 focus:border-orange-300 disabled:opacity-50" />
            <button onClick={handleSend} disabled={!input.trim() || sending}
              className="p-3 bg-orange-500 text-white rounded-xl hover:bg-orange-600 disabled:opacity-40 transition-all">
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}