'use client'

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, Plus, MessageSquare, Send, Loader2, FileText } from 'lucide-react'

interface Message {
  id: string; role: 'user' | 'ai'; content: string; source?: string; timestamp: Date
}

interface Thread {
  id: string; title: string; createdAt: Date
}

export default function HomePage() {
  const router = useRouter()
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSelectThread = async (threadId: string) => {
    setActiveThreadId(threadId); setMessages([])
    const token = localStorage.getItem('bitewise_auth_token')
    try {
      const res = await fetch(`http://localhost:8000/rag/threads/${threadId}`, { headers: { Authorization: `Bearer ${token}` } })
      const data = await res.json()
      if (Array.isArray(data)) {
        const msgs: Message[] = []
        data.forEach((m: any) => {
          msgs.push({ id: `q${m.id}`, role: 'user', content: m.question, timestamp: new Date(m.created_at) })
          msgs.push({ id: `a${m.id}`, role: 'ai', content: m.answer, source: m.sources ? JSON.parse(m.sources)[0]?.document_name : undefined, timestamp: new Date(m.created_at) })
        })
        setMessages(msgs.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime()))
      }
    } catch (err) { console.error(err) }
  }

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    const role = localStorage.getItem('user_role')
    if (!token) { router.push('/'); return }
    if (role === 'admin') { router.push('/admin'); return }
    fetch('http://localhost:8000/rag/threads', { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          const tl = data.map((t: any) => ({ id: t.thread_id, title: t.title || t.thread_id, createdAt: new Date() }))
          setThreads(tl); handleSelectThread(tl[0].id)
        }
      }).catch(console.error)
  }, [router])

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  const handleSend = async () => {
    if (!input.trim() || sending) return
    const token = localStorage.getItem('bitewise_auth_token')
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: input, timestamp: new Date() }
    setMessages(prev => [...prev, userMsg]); setInput(''); setSending(true)
    try {
      const res = await fetch('http://localhost:8000/rag/query', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ question: userMsg.content, top_k: 3, conversation_id: activeThreadId || undefined }),
      })
      const data = await res.json()
      const aiMsg: Message = { id: (Date.now() + 1).toString(), role: 'ai', content: data.answer, source: data.sources?.[0]?.document_name, timestamp: new Date() }
      setMessages(prev => [...prev, aiMsg])
      if (!activeThreadId) {
        const nt = { id: `thread-${Date.now()}`, title: userMsg.content.substring(0, 40), createdAt: new Date() }
        setActiveThreadId(nt.id); setThreads(prev => [nt, ...prev])
      }
    } catch { } finally { setSending(false) }
  }

  const handleLogout = () => { localStorage.clear(); router.push('/') }

  return (
    <div style={{height:'100vh', display:'flex', fontFamily:"'Inter', sans-serif"}}>
      {/* LEFT SIDEBAR — Gradient */}
      <div style={{
        width:280, background:'linear-gradient(180deg,#FFB25B,#FF8D5C)',
        display:'flex', flexDirection:'column', padding:'24px 20px', color:'white', flexShrink:0
      }}>
        <div style={{display:'flex', alignItems:'center', gap:10, marginBottom:28}}>
          <div style={{width:36, height:36, borderRadius:'50%', background:'rgba(255,255,255,.25)', display:'flex', justifyContent:'center', alignItems:'center', fontSize:18}}>🌸</div>
          <span style={{fontSize:20, fontWeight:700}}>BiteWise</span>
        </div>

        <button onClick={() => { setActiveThreadId(null); setMessages([]) }}
          style={{width:'100%', padding:'12px', borderRadius:14, border:'none', background:'rgba(255,255,255,.2)', color:'white', fontWeight:600, fontSize:14, cursor:'pointer', marginBottom:24, display:'flex', alignItems:'center', justifyContent:'center', gap:8}}>
          <Plus size={18} /> New Chat
        </button>

        <div style={{flex:1, overflowY:'auto'}}>
          {threads.map(t => (
            <div key={t.id} onClick={() => handleSelectThread(t.id)}
              style={{padding:'10px 14px', borderRadius:12, marginBottom:6, cursor:'pointer',
                background: activeThreadId === t.id ? 'rgba(255,255,255,.25)' : 'transparent',
                fontSize:13, fontWeight: activeThreadId === t.id ? 600 : 400, transition:'0.2s',
                whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis'}}>
              <MessageSquare size={14} style={{display:'inline', marginRight:6, opacity:.7}} />
              {t.title}
            </div>
          ))}
        </div>

        <button onClick={handleLogout}
          style={{padding:'10px', borderRadius:12, border:'none', background:'rgba(255,255,255,.15)', color:'white', fontSize:13, cursor:'pointer', marginTop:16, display:'flex', alignItems:'center', gap:6, width:'100%'}}>
          <LogOut size={16} /> Logout
        </button>
      </div>

      {/* RIGHT CHAT AREA */}
      <div style={{flex:1, display:'flex', flexDirection:'column', background:'#fafafa'}}>
        {/* Header */}
        <div style={{padding:'16px 24px', background:'white', borderBottom:'1px solid #f0f0f0', display:'flex', alignItems:'center', gap:10}}>
          <div style={{width:36, height:36, borderRadius:'50%', background:'#EFEAFB', display:'flex', alignItems:'center', justifyContent:'center'}}>
            <ChefHat size={20} color="#FF8D5C" />
          </div>
          <div>
            <div style={{fontWeight:600, fontSize:15, color:'#111'}}>{activeThreadId ? 'Conversation' : 'New Chat'}</div>
            <div style={{fontSize:12, color:'#999'}}>Ask about menu, prices & offers</div>
          </div>
        </div>

        {/* Messages */}
        <div style={{flex:1, overflowY:'auto', padding:'20px 24px'}}>
          {messages.length === 0 ? (
            <div style={{height:'100%', display:'flex', flexDirection:'column', justifyContent:'center', alignItems:'center', textAlign:'center'}}>
              <div style={{width:80, height:80, borderRadius:'50%', background:'#FFF0E5', display:'flex', alignItems:'center', justifyContent:'center', marginBottom:16}}>
                <ChefHat size={36} color="#FF8D5C" />
              </div>
              <h2 style={{fontSize:20, fontWeight:700, color:'#111', marginBottom:8}}>Welcome to BiteWise! 🍽️</h2>
              <p style={{color:'#999', maxWidth:300}}>Ask about our authentic Pakistani menu, prices, offers, or policies.</p>
            </div>
          ) : (
            messages.map(m => (
              <div key={m.id} style={{display:'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start', marginBottom:16}}>
                <div style={{
                  maxWidth:'70%', padding:'12px 18px', borderRadius: m.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                  background: m.role === 'user' ? '#FF8D5C' : 'white', color: m.role === 'user' ? 'white' : '#333',
                  boxShadow: m.role === 'user' ? 'none' : '0 2px 8px rgba(0,0,0,0.04)', fontSize:14, lineHeight:1.5
                }}>
                  {m.content}
                  {m.source && <div style={{marginTop:8, paddingTop:8, borderTop:'1px solid rgba(0,0,0,0.06)', fontSize:11, opacity:.7, display:'flex', alignItems:'center', gap:4}}><FileText size={12} />{m.source}</div>}
                </div>
              </div>
            ))
          )}
          {sending && <div style={{display:'flex', justifyContent:'flex-start', marginBottom:16}}><Loader2 size={18} style={{color:'#FF8D5C', animation:'spin 1s linear infinite'}} /></div>}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div style={{padding:'16px 24px', background:'white', borderTop:'1px solid #f0f0f0'}}>
          <div style={{display:'flex', gap:12, maxWidth:700, margin:'0 auto'}}>
            <input type="text" value={input} onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() } }}
              placeholder="Ask about menu, prices, or anything else..." disabled={sending}
              style={{flex:1, height:48, borderRadius:24, border:'none', background:'#F5F5F5', padding:'0 20px', fontSize:14, outline:'none'}} />
            <button onClick={handleSend} disabled={!input.trim() || sending}
              style={{width:48, height:48, borderRadius:'50%', border:'none', background:'#FF8D5C', color:'white', cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center', opacity: !input.trim()||sending ? 0.5 : 1}}>
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}