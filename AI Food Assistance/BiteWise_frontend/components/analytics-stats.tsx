import { MessageSquare, FileText, MessageCircle, Users, TrendingUp } from 'lucide-react'

interface StatCard {
  label: string
  value: number
  change: number
  icon: React.ReactNode
  color: string
}

export default function AnalyticsStats() {
  const stats: StatCard[] = [
    {
      label: 'Total Queries',
      value: 342,
      change: 12,
      icon: <MessageSquare className="w-6 h-6" />,
      color: 'from-primary to-accent',
    },
    {
      label: 'Documents',
      value: 12,
      change: 8,
      icon: <FileText className="w-6 h-6" />,
      color: 'from-accent to-secondary',
    },
    {
      label: 'Active Threads',
      value: 87,
      change: 15,
      icon: <MessageCircle className="w-6 h-6" />,
      color: 'from-secondary to-primary',
    },
    {
      label: 'Total Users',
      value: 45,
      change: 20,
      icon: <Users className="w-6 h-6" />,
      color: 'from-primary via-accent to-secondary',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {stats.map((stat, index) => (
        <div
          key={index}
          className="bg-card border border-border rounded-xl p-6 hover:border-primary/50 transition-all duration-200"
        >
          <div className="flex items-start justify-between mb-4">
            <div className={`p-3 bg-gradient-to-br ${stat.color} rounded-lg text-card`}>
              {stat.icon}
            </div>
            <div className="flex items-center gap-1 bg-green-500/10 px-2 py-1 rounded-full">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-xs font-semibold text-green-500">{stat.change}%</span>
            </div>
          </div>

          <h3 className="text-muted-foreground text-sm font-medium mb-1">
            {stat.label}
          </h3>
          <p className="text-3xl md:text-4xl font-bold text-foreground">
            {stat.value.toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  )
}
