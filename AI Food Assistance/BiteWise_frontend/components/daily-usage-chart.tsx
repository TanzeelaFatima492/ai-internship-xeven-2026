'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

const data = [
  { date: 'Dec 1', queries: 45 },
  { date: 'Dec 2', queries: 52 },
  { date: 'Dec 3', queries: 48 },
  { date: 'Dec 4', queries: 61 },
  { date: 'Dec 5', queries: 55 },
  { date: 'Dec 6', queries: 67 },
  { date: 'Dec 7', queries: 72 },
]

export default function DailyUsageChart() {
  return (
    <div className="bg-card border border-border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-foreground mb-2">Daily Usage Trend</h3>
        <p className="text-sm text-muted-foreground">
          Queries per day over the last 7 days
        </p>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
          <XAxis
            dataKey="date"
            stroke="rgb(var(--color-muted-foreground))"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            stroke="rgb(var(--color-muted-foreground))"
            style={{ fontSize: '12px' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgb(var(--color-card))',
              border: '1px solid rgb(var(--color-border))',
              borderRadius: '8px',
              color: 'rgb(var(--color-foreground))',
            }}
          />
          <Legend wrapperStyle={{ color: 'rgb(var(--color-foreground))' }} />
          <Line
            type="monotone"
            dataKey="queries"
            stroke="url(#colorGradient)"
            strokeWidth={3}
            dot={{
              fill: 'rgb(var(--color-primary))',
              r: 5,
            }}
            activeDot={{
              r: 7,
            }}
          />
          <defs>
            <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="rgb(var(--color-primary))" />
              <stop offset="95%" stopColor="rgb(var(--color-accent))" />
            </linearGradient>
          </defs>
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
