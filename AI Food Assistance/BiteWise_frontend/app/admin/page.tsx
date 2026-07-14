'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import AnalyticsDashboard from '@/components/analytics-dashboard'
import PDFUploadArea from '@/components/pdf-upload-area'
import ThreadList from '@/components/thread-list'
import { LogOut, BarChart3, FileUp, MessageSquare, Download, ChefHat } from 'lucide-react'

type AdminTab = 'dashboard' | 'upload' | 'analytics' | 'threads' | 'export'

interface AdminStats {
  totalDocuments: number; totalQueries: number; totalThreads: number; activeUsers: number
}

export default function AdminPage() {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState<AdminTab>('dashboard')
  const [stats, setStats] = useState<AdminStats>({ totalDocuments: 0, totalQueries: 0, totalThreads: 0, activeUsers: 0 })

  const downloadCSV = async (endpoint: string, filename: string) => {
  const token = localStorage.getItem('bitewise_auth_token')
  try {
    const res = await fetch(`http://localhost:8000/${endpoint}`, { headers: { Authorization: `Bearer ${token}` } })
    const data = await res.json()
    const items = Array.isArray(data) ? data : [data]
    if (items.length === 0) { alert('No data to export'); return }
    
    const headers = Object.keys(items[0]).join(',')
    const rows = items.map((item: any) => Object.values(item).map(v => `"${String(v).replace(/"/g,'""')}"`).join(',')).join('\n')
    const csv = headers + '\n' + rows
    
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = `${filename}-${new Date().toISOString().split('T')[0]}.csv`; a.click()
    URL.revokeObjectURL(url)
  } catch { alert('Download failed') }
}

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    const role = localStorage.getItem('user_role')
    if (!token) { router.push('/'); return }
    if (role !== 'admin') { router.push('/home'); return }
    fetch('http://localhost:8000/analytics/overview', { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(data => setStats({
        totalDocuments: data.total_documents || 0, totalQueries: data.total_queries || 0,
        totalThreads: data.total_threads || 0, activeUsers: data.total_queries || 0
      })).catch(console.error)
  }, [router])

  const handleLogout = () => { localStorage.clear(); router.push('/') }

  const navItems = [
    { id: 'dashboard' as AdminTab, label: 'Dashboard', icon: BarChart3 },
    { id: 'upload' as AdminTab, label: 'Upload PDF', icon: FileUp },
    { id: 'analytics' as AdminTab, label: 'Analytics', icon: BarChart3 },
    { id: 'threads' as AdminTab, label: 'Threads', icon: MessageSquare },
    { id: 'export' as AdminTab, label: 'Export', icon: Download },
  ]

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
            <div style={{fontSize:11, opacity:.8}}>Admin Panel</div>
          </div>
        </div>

        {navItems.map(item => {
          const Icon = item.icon
          return (
            <button key={item.id} onClick={() => setActiveTab(item.id)}
              style={{
                width:'100%', padding:'12px 16px', borderRadius:12, marginBottom:6,
                border:'none', cursor:'pointer', display:'flex', alignItems:'center', gap:10,
                background: activeTab === item.id ? 'rgba(255,255,255,.25)' : 'transparent',
                color:'white', fontSize:14, fontWeight: activeTab === item.id ? 600 : 400,
                transition:'0.2s', textAlign:'left'
              }}>
              <Icon size={18} /> {item.label}
            </button>
          )
        })}

        <button onClick={handleLogout}
          style={{padding:'10px', borderRadius:12, border:'none', background:'rgba(255,255,255,.15)', color:'white', fontSize:13, cursor:'pointer', marginTop:'auto', display:'flex', alignItems:'center', gap:6, width:'100%'}}>
          <LogOut size={16} /> Logout
        </button>
      </div>

      {/* RIGHT CONTENT */}
      <div style={{flex:1, display:'flex', flexDirection:'column', background:'#fafafa', overflow:'auto'}}>
        <div style={{padding:'16px 28px', background:'white', borderBottom:'1px solid #f0f0f0'}}>
          <h1 style={{fontSize:20, fontWeight:700, color:'#111', margin:0}}>Admin Dashboard</h1>
          <p style={{fontSize:12, color:'#999', margin:'2px 0 0 0'}}>Manage your restaurant AI system</p>
        </div>

        <div style={{flex:1, padding:'28px', overflowY:'auto'}}>
          {activeTab === 'dashboard' && (
            <div>
              <div style={{display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap:20, marginBottom:32}}>
                <div style={{background:'white', borderRadius:20, padding:'24px 20px', border:'1px solid #f0f0f0', display:'flex', alignItems:'center', gap:16}}>
                  <div style={{width:52, height:52, borderRadius:14, background:'#FFF0E5', display:'flex', alignItems:'center', justifyContent:'center'}}><FileUp size={24} color="#FF8D5C" /></div>
                  <div><div style={{fontSize:26, fontWeight:700, color:'#111'}}>{stats.totalDocuments}</div><div style={{fontSize:13, color:'#999'}}>Documents</div></div>
                </div>
                <div style={{background:'white', borderRadius:20, padding:'24px 20px', border:'1px solid #f0f0f0', display:'flex', alignItems:'center', gap:16}}>
                  <div style={{width:52, height:52, borderRadius:14, background:'#E8F5E9', display:'flex', alignItems:'center', justifyContent:'center'}}><MessageSquare size={24} color="#4CAF50" /></div>
                  <div><div style={{fontSize:26, fontWeight:700, color:'#111'}}>{stats.totalQueries}</div><div style={{fontSize:13, color:'#999'}}>Queries</div></div>
                </div>
                <div style={{background:'white', borderRadius:20, padding:'24px 20px', border:'1px solid #f0f0f0', display:'flex', alignItems:'center', gap:16}}>
                  <div style={{width:52, height:52, borderRadius:14, background:'#E3F2FD', display:'flex', alignItems:'center', justifyContent:'center'}}><BarChart3 size={24} color="#2196F3" /></div>
                  <div><div style={{fontSize:26, fontWeight:700, color:'#111'}}>{stats.totalThreads}</div><div style={{fontSize:13, color:'#999'}}>Threads</div></div>
                </div>
                <div style={{background:'white', borderRadius:20, padding:'24px 20px', border:'1px solid #f0f0f0', display:'flex', alignItems:'center', gap:16}}>
                  <div style={{width:52, height:52, borderRadius:14, background:'#FCE4EC', display:'flex', alignItems:'center', justifyContent:'center'}}><Download size={24} color="#E91E63" /></div>
                  <div><div style={{fontSize:26, fontWeight:700, color:'#111'}}>{stats.activeUsers}</div><div style={{fontSize:13, color:'#999'}}>Users</div></div>
                </div>
              </div>
              <div style={{background:'white', borderRadius:20, padding:28, border:'1px solid #f0f0f0'}}>
                <h3 style={{fontSize:18, fontWeight:600, color:'#111', marginBottom:20}}>Quick Overview</h3>
                <div style={{display:'grid', gridTemplateColumns:'repeat(2, 1fr)', gap:24}}>
                  <div style={{padding:20, background:'#fafafa', borderRadius:14}}>
                    <div style={{fontSize:13, color:'#999', marginBottom:8}}>Storage Used</div>
                    <div style={{fontSize:28, fontWeight:700, color:'#111'}}>{stats.totalDocuments * 2.5} MB</div>
                    <div style={{marginTop:12, height:6, background:'#f0f0f0', borderRadius:3}}><div style={{width:`${Math.min(stats.totalDocuments*5,100)}%`, height:'100%', background:'linear-gradient(90deg,#FFB25B,#FF8D5C)', borderRadius:3}} /></div>
                  </div>
                  <div style={{padding:20, background:'#fafafa', borderRadius:14}}>
                    <div style={{fontSize:13, color:'#999', marginBottom:8}}>Response Rate</div>
                    <div style={{fontSize:28, fontWeight:700, color:'#111'}}>98%</div>
                    <div style={{marginTop:12, height:6, background:'#f0f0f0', borderRadius:3}}><div style={{width:'98%', height:'100%', background:'linear-gradient(90deg,#4CAF50,#8BC34A)', borderRadius:3}} /></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'upload' && <PDFUploadArea onUploadComplete={() => setStats(prev => ({ ...prev, totalDocuments: prev.totalDocuments + 1 }))} />}

          {activeTab === 'analytics' && <AnalyticsDashboard />}

          {activeTab === 'threads' && <ThreadList />}

          {activeTab === 'export' && (
            <div>
              <h2 style={{fontSize:20, fontWeight:700, color:'#111', marginBottom:20}}>Export Data</h2>
              <div style={{display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:16}}>
                {[
                  { label:'Overview Report', endpoint:'analytics/overview', file:'bitewise-overview' },
                  { label:'Popular Questions', endpoint:'analytics/popular-questions?limit=50', file:'bitewise-questions' },
                  { label:'Thread List', endpoint:'rag/threads', file:'bitewise-threads' },
                ].map((item, i) => (
                  <div key={i} onClick={() => downloadCSV(item.endpoint, item.file)}
                    style={{padding:24, borderRadius:16, border:'1px solid #f0f0f0', background:'white', textAlign:'center', cursor:'pointer'}}>
                    <Download size={28} style={{color:'#FF8D5C', marginBottom:12}} />
                    <div style={{fontWeight:600, fontSize:15, color:'#111'}}>{item.label}</div>
                    <div style={{fontSize:12, color:'#999', marginTop:4}}>Download JSON</div>
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