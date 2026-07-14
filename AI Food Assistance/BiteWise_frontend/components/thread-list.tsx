'use client'

import { useEffect, useState } from 'react'
import { MessageSquare, ChevronRight } from 'lucide-react'

interface Thread {
  thread_id: string
  title?: string
}

export default function ThreadList() {
  const [threads, setThreads] = useState<Thread[]>([])

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/rag/threads', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => setThreads(Array.isArray(data) ? data : []))
    .catch(console.error)
  }, [])

  return (
    <div>
      <h2 style={{fontSize:20, fontWeight:700, color:'#111', marginBottom:20}}>Conversation Threads</h2>
      
      {threads.length === 0 ? (
        <div style={{background:'white', borderRadius:16, padding:40, border:'1px solid #f0f0f0', textAlign:'center'}}>
          <MessageSquare size={40} style={{color:'#ddd', marginBottom:12}} />
          <p style={{color:'#999', fontSize:14}}>No conversation threads yet</p>
          <p style={{color:'#ccc', fontSize:12, marginTop:4}}>Customer queries will appear here</p>
        </div>
      ) : (
        <div style={{display:'flex', flexDirection:'column', gap:8}}>
          {threads.map((t, i) => (
            <div key={i} style={{
              background:'white', borderRadius:14, padding:'16px 20px', border:'1px solid #f0f0f0',
              display:'flex', alignItems:'center', justifyContent:'space-between',
              cursor:'pointer', transition:'0.2s'
            }}>
              <div style={{display:'flex', alignItems:'center', gap:12}}>
                <div style={{width:40, height:40, borderRadius:10, background:'#FFF0E5', display:'flex', alignItems:'center', justifyContent:'center'}}>
                  <MessageSquare size={18} color="#FF8D5C" />
                </div>
                <div>
                  <div style={{fontWeight:600, fontSize:14, color:'#111'}}>{t.title || t.thread_id}</div>
                  <div style={{fontSize:12, color:'#999', marginTop:2}}>Thread ID: {t.thread_id}</div>
                </div>
              </div>
              <ChevronRight size={18} style={{color:'#ccc'}} />
            </div>
          ))}
        </div>
      )}

      <div style={{marginTop:16, fontSize:13, color:'#999', textAlign:'center'}}>
        Total: {threads.length} thread{threads.length !== 1 ? 's' : ''}
      </div>
    </div>
  )
}