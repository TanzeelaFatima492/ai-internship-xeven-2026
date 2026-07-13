import { TrendingUp } from 'lucide-react'

export default function AnalyticsHeader() {
  return (
    <div className="mb-8">
      <div className="bg-gradient-to-r from-primary/10 via-accent/10 to-secondary/10 border border-border rounded-2xl p-6 md:p-8">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-gradient-to-br from-primary to-accent rounded-lg">
            <TrendingUp className="w-6 h-6 text-card" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
              Performance Analytics
            </h2>
            <p className="text-muted-foreground">
              Track user engagement, popular queries, and system performance metrics
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
