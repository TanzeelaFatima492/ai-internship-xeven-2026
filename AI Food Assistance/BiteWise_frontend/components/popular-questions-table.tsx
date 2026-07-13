import { TrendingUp } from 'lucide-react'

interface Question {
  question: string
  count: number
  percentage: number
}

const questions: Question[] = [
  { question: "What's the biryani price?", count: 145, percentage: 42.4 },
  { question: 'Do you have vegetarian options?', count: 98, percentage: 28.7 },
  { question: 'What are delivery hours?', count: 67, percentage: 19.6 },
  { question: 'Tell me about offers', count: 45, percentage: 13.2 },
  { question: 'How to place an order?', count: 32, percentage: 9.4 },
]

export default function PopularQuestionsTable() {
  return (
    <div className="bg-card border border-border rounded-xl p-6 h-full">
      <div className="mb-4">
        <h3 className="text-lg font-bold text-foreground mb-2">Popular Questions</h3>
        <p className="text-sm text-muted-foreground">Top asked questions</p>
      </div>

      <div className="space-y-3">
        {questions.map((q, index) => (
          <div key={index} className="p-3 rounded-lg bg-background/50 hover:bg-background transition-colors">
            <div className="flex items-start justify-between gap-2 mb-2">
              <p className="text-sm font-medium text-foreground line-clamp-2 flex-1">
                {q.question}
              </p>
              <span className="flex items-center gap-1 px-2 py-1 bg-primary/10 rounded text-primary text-xs font-semibold whitespace-nowrap">
                <TrendingUp size={12} />
                {q.count}
              </span>
            </div>
            <div className="w-full bg-background rounded-full h-2 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary via-accent to-secondary transition-all duration-300"
                style={{ width: `${q.percentage}%` }}
              ></div>
            </div>
            <p className="text-xs text-muted-foreground mt-1">{q.percentage}% of total</p>
          </div>
        ))}
      </div>
    </div>
  )
}
