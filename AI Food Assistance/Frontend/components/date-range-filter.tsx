'use client'

import { useState } from 'react'
import { Calendar } from 'lucide-react'
import { format } from 'date-fns'

interface DateRange {
  startDate: Date
  endDate: Date
}

interface DateRangeFilterProps {
  dateRange: DateRange
  onDateRangeChange: (range: DateRange) => void
}

export default function DateRangeFilter({
  dateRange,
  onDateRangeChange,
}: DateRangeFilterProps) {
  const [isOpen, setIsOpen] = useState(false)

  const presets = [
    {
      label: 'Last 7 Days',
      getValue: () => ({
        startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
        endDate: new Date(),
      }),
    },
    {
      label: 'Last 30 Days',
      getValue: () => ({
        startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        endDate: new Date(),
      }),
    },
    {
      label: 'Last 90 Days',
      getValue: () => ({
        startDate: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000),
        endDate: new Date(),
      }),
    },
    {
      label: 'This Year',
      getValue: () => ({
        startDate: new Date(new Date().getFullYear(), 0, 1),
        endDate: new Date(),
      }),
    },
  ]

  const handlePreset = (getValue: () => DateRange) => {
    const newRange = getValue()
    onDateRangeChange(newRange)
    setIsOpen(false)
  }

  return (
    <div className="relative w-full sm:w-auto">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full sm:w-auto flex items-center gap-2 px-4 py-2 bg-card border border-border rounded-lg hover:border-primary/50 transition-colors text-foreground"
      >
        <Calendar size={18} />
        <span className="text-sm font-medium">
          {format(dateRange.startDate, 'MMM dd')} - {format(dateRange.endDate, 'MMM dd')}
        </span>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-48 bg-card border border-border rounded-lg shadow-lg z-50 p-3 space-y-2">
          {presets.map((preset, index) => (
            <button
              key={index}
              onClick={() => handlePreset(preset.getValue)}
              className="w-full px-3 py-2 text-sm text-foreground hover:bg-background rounded-lg transition-colors text-left font-medium"
            >
              {preset.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
