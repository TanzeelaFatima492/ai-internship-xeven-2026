'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function DailyUsageChart() {
  const [data, setData] = useState<any[]>([])

  useEffect(() => {
    const token = localStorage.getItem('bitewise_auth_token')
    fetch('http://localhost:8000/analytics/daily-usage', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(d => setData(d))
    .catch(console.error)
  }, [])

  if (data.length === 0) return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      <h3 className="text-lg font-bold text-gray-900">Daily Usage Trend</h3>
      <p className="text-gray-400 text-center py-8">No data available</p>
    </div>
  )

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Daily Usage Trend</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="date" stroke="#6B7280" fontSize={12} />
          <YAxis stroke="#6B7280" fontSize={12} />
          <Tooltip contentStyle={{ backgroundColor: '#FFF', border: '1px solid #E5E7EB', borderRadius: '8px' }} />
          <Line type="monotone" dataKey="queries" stroke="#F97316" strokeWidth={3} dot={{ fill: '#F97316', r: 5 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}