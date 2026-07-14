'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { LogOut, ChefHat, Download, BarChart3 } from 'lucide-react'

interface AnalyticsData {
  overview: { total_queries: number; total_documents: number; total_chunks: number; total_threads: number }
  popularQuestions: { question: string; count: number }[]
  recentQueries: { id: number; question: string; answer: string; created_at: string }[]
}

export default function AnalyticsPage() {
  const router = useRouter()
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    const role = localStorage.getItem('user_role')
    if (!token) { router.push('/'); return }
    if (role !== 'admin') { router.push('/home'); return }

    Promise.all([
      fetch('http://localhost:8000/analytics/overview', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/popular-questions?limit=10', { headers: { Authorization: `Bearer ${token}` } }),
      fetch('http://localhost:8000/analytics/recent-queries?limit=10', { headers: { Authorization: `Bearer ${token}` } }),
    ])
      .then(responses => Promise.all(responses.map(r => r.json())))
      .then(([overview, popularQuestions, recentQueries]) => {
        setData({ overview, popularQuestions, recentQueries })
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [router])

  const handleExport = () => {
    if (!data) return
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = `bitewise-analytics-${new Date().toISOString().split('T')[0]}.json`; a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) return (
    <div style={{height:'100vh', display:'flex', alignItems:'center', justifyContent:'center', background:'#fafafa'}}>
      <div style={{width:36, height:36, borderRadius:'50%', border:'3px solid #FF8D5C', borderTopColor:'transparent', animation:'spin 1s linear infinite'}} />
    </div>
  )

  return (
    <div style={{height:'100vh', display:'flex', fontFamily:"'Inter', sans-serif"}}>
      {/* LEFT SIDEBAR */}
      <div style={{
        width:260, background:'linear-gradient(180deg,#FFB25B,#FF8D5C)',
        display:'flex', flexDirection:'column', padding:'24px 18px', color:'white', flexShrink:0
      }}>
        <div style={{display:'flex', alignItems:'center', gap:10, marginBottom:32}}>
          <div style={{width:36, height:36, borderRadius:'50%', background:'rgba(255,255,255,.25)', display:'flex', justifyContent:'center', alignItems:'center', fontSize:18}}>🌸</div>
          <div>
            <div style={{fontSize:18, fontWeight:700}}>BiteWise</div>
            <div style={{fontSize:11, opacity:.8}}>Analytics</div>
          </div>
        </div>

        <div style={{flex:1}} />

        <button onClick={() => { localStorage.clear(); router.push('/') }}
          style={{padding:'10px', borderRadius:12, border:'none', background:'rgba(255,255,255,.15)', color:'white', fontSize:13, cursor:'pointer', display:'flex', alignItems:'center', gap:6, width:'100%'}}>
          <LogOut size={16} /> Logout
        </button>
      </div>

      {/* RIGHT CONTENT */}
      <div style={{flex:1, display:'flex', flexDirection:'column', background:'#fafafa', overflow:'auto'}}>
        <div style={{padding:'16px 28px', background:'white', borderBottom:'1px solid #f0f0f0', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
          <div>
            <h1 style={{fontSize:20, fontWeight:700, color:'#111', margin:0}}>Analytics Dashboard</h1>
            <p style={{fontSize:12, color:'#999', margin:'2px 0 0 0'}}>Performance metrics & insights</p>
          </div>
          <button onClick={handleExport}
            style={{padding:'10px 18px', borderRadius:25, border:'none', background:'#FF8D5C', color:'white', fontWeight:600, fontSize:13, cursor:'pointer', display:'flex', alignItems:'center', gap:6}}>
            <Download size={16} /> Export JSON
          </button>
        </div>

        <div style={{flex:1, padding:'28px', overflowY:'auto'}}>
          {data && (
            <div style={{maxWidth:900}}>
              {/* Stats Cards */}
              <div style={{display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap:16, marginBottom:28}}>
                {[
                  { label:'Total Queries', value:data.overview.total_queries, icon:'💬' },
                  { label:'Documents', value:data.overview.total_documents, icon:'📄' },
                  { label:'Chunks', value:data.overview.total_chunks, icon:'🧩' },
                  { label:'Threads', value:data.overview.total_threads, icon:'🧵' },
                ].map((s, i) => (
                  <div key={i} style={{background:'white', borderRadius:16, padding:20, border:'1px solid #f0f0f0'}}>
                    <div style={{fontSize:28, marginBottom:8}}>{s.icon}</div>
                    <div style={{fontSize:28, fontWeight:700, color:'#111'}}>{s.value}</div>
                    <div style={{fontSize:13, color:'#999', marginTop:4}}>{s.label}</div>
                  </div>
                ))}
              </div>

              {/* Popular Questions */}
              <div style={{background:'white', borderRadius:16, padding:24, border:'1px solid #f0f0f0', marginBottom:24}}>
                <h3 style={{fontSize:16, fontWeight:600, color:'#111', marginBottom:16}}>Popular Questions</h3>
                {data.popularQuestions.slice(0, 5).map((q, i) => (
                  <div key={i} style={{display:'flex', justifyContent:'space-between', padding:'12px 0', borderBottom:'1px solid #f5f5f5'}}>
                    <span style={{fontSize:14, color:'#444'}}>{q.question}</span>
                    <span style={{background:'#FFF0E5', color:'#FF8D5C', padding:'4px 12px', borderRadius:20, fontSize:13, fontWeight:600}}>{q.count}x</span>
                  </div>
                ))}
              </div>

              {/* Recent Queries */}
              <div style={{background:'white', borderRadius:16, padding:24, border:'1px solid #f0f0f0'}}>
                <h3 style={{fontSize:16, fontWeight:600, color:'#111', marginBottom:16}}>Recent Queries</h3>
                {data.recentQueries.slice(0, 5).map(q => (
                  <div key={q.id} style={{padding:14, background:'#fafafa', borderRadius:12, marginBottom:10}}>
                    <p style={{fontSize:14, fontWeight:600, color:'#111', margin:'0 0 4px 0'}}>Q: {q.question}</p>
                    <p style={{fontSize:13, color:'#666', margin:'0 0 4px 0'}}>A: {q.answer?.substring(0, 80)}...</p>
                    <p style={{fontSize:11, color:'#bbb', margin:0}}>{new Date(q.created_at).toLocaleString()}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}