'use client'

import { BarChart3 } from 'lucide-react'

interface PopularQuestion {
  question: string
  count: number
  percentage: number
}

const popularQuestions: PopularQuestion[] = [
  { question: 'What are your prices?', count: 84, percentage: 24 },
  { question: 'Do you deliver?', count: 72, percentage: 21 },
  { question: 'Menu recommendations', count: 56, percentage: 16 },
  { question: 'Dietary restrictions', count: 45, percentage: 13 },
  { question: 'Current offers', count: 38, percentage: 11 },
  { question: 'Reservation info', count: 28, percentage: 8 },
  { question: 'Timing/Hours', count: 19, percentage: 7 },
]

export default function PopularQuestionsChart() {
  return (
    <div className="bg-card border border-border rounded-xl overflow-hidden">
      <div className="p-6 border-b border-border">
        <h3 className="text-lg font-semibold text-foreground">Popular Questions</h3>
        <p className="text-sm text-muted-foreground">Most frequently asked questions by users</p>
      </div>

      <div className="p-6 space-y-6">
        {popularQuestions.map((item, idx) => (
          <div key={idx} className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-foreground font-medium truncate pr-4">{item.question}</span>
              <span className="text-muted-foreground font-semibold flex-shrink-0">{item.count}</span>
            </div>
            <div className="relative w-full h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-300 bg-gradient-to-r from-primary via-accent to-secondary"
                style={{ width: `${item.percentage}%` }}
              />
            </div>
            <div className="text-xs text-muted-foreground text-right">{item.percentage}%</div>
          </div>
        ))}
      </div>

      <div className="px-6 py-4 border-t border-border bg-muted/20">
        <button className="w-full text-center text-sm font-medium text-primary hover:text-accent transition-colors py-2">
          View Full Analytics →
        </button>
      </div>
    </div>
  )
}
