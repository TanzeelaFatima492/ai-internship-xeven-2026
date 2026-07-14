'use client'

import { useEffect, useState } from 'react'
import { MessageSquare, ChevronRight } from 'lucide-react'

interface Thread {
  thread_id: string
  title?: string
}

export default function ThreadList() {
  const [threads, setThreads] = useState<Thread[]>([])
  const [counts, setCounts] = useState<Record<string, number>>({})

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/rag/threads', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(async (data) => {
      if (Array.isArray(data)) {
        setThreads(data)
        // Get message count for each thread
        const countsMap: Record<string, number> = {}
        for (const t of data) {
          try {
            const res = await fetch(`http://localhost:8000/rag/threads/${t.thread_id}`, {
              headers: { Authorization: `Bearer ${token}` }
            })
            const msgs = await res.json()
            countsMap[t.thread_id] = Array.isArray(msgs) ? msgs.length : 0
          } catch { countsMap[t.thread_id] = 0 }
        }
        setCounts(countsMap)
      }
    })
    .catch(console.error)
  }, [])

  return (
    <div>
      <h2 style={{fontSize:20, fontWeight:700, color:'#111', marginBottom:20}}>Conversation Threads</h2>
      
      {threads.length === 0 ? (
        <div style={{background:'white', borderRadius:16, padding:40, border:'1px solid #f0f0f0', textAlign:'center'}}>
          <MessageSquare size={40} style={{color:'#ddd', marginBottom:12}} />
          <p style={{color:'#999', fontSize:14}}>No conversation threads yet</p>
        </div>
      ) : (
        <div style={{display:'flex', flexDirection:'column', gap:8}}>
          {threads.map((t, i) => (
            <div key={i} style={{
              background:'white', borderRadius:14, padding:'16px 20px', border:'1px solid #f0f0f0',
              display:'flex', alignItems:'center', justifyContent:'space-between'
            }}>
              <div style={{display:'flex', alignItems:'center', gap:12}}>
                <div style={{width:40, height:40, borderRadius:10, background:'#FFF0E5', display:'flex', alignItems:'center', justifyContent:'center'}}>
                  <MessageSquare size={18} color="#FF8D5C" />
                </div>
                <div>
                  <div style={{fontWeight:600, fontSize:14, color:'#111'}}>{t.title || t.thread_id}</div>
                  <div style={{fontSize:12, color:'#999', marginTop:2}}>
                    {counts[t.thread_id] || 0} message{counts[t.thread_id] !== 1 ? 's' : ''}
                  </div>
                </div>
              </div>
              <div style={{display:'flex', alignItems:'center', gap:12}}>
                <span style={{background:'#FFF0E5', color:'#FF8D5C', padding:'4px 10px', borderRadius:20, fontSize:12, fontWeight:600}}>
                  {counts[t.thread_id] || 0}
                </span>
                <ChevronRight size={18} style={{color:'#ccc'}} />
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{marginTop:16, fontSize:13, color:'#999', textAlign:'center'}}>
        Total: {threads.length} thread{threads.length !== 1 ? 's' : ''} • {Object.values(counts).reduce((a,b) => a+b, 0)} messages
      </div>
    </div>
  )
}