'use client'

import { useState } from 'react'
import { Send } from 'lucide-react'

interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSend: (message: string) => void
  disabled?: boolean
  placeholder?: string
}

export default function ChatInput({
  value,
  onChange,
  onSend,
  disabled = false,
  placeholder = 'Type your message...',
}: ChatInputProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (value.trim() && !disabled) {
      onSend(value)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Handle CJK IME composition
    if (e.nativeEvent.isComposing || e.keyCode === 229) return

    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (value.trim() && !disabled) {
        onSend(value)
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 md:gap-3">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        rows={1}
        className="flex-1 bg-background border border-border rounded-xl px-4 md:px-5 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 disabled:opacity-50 disabled:cursor-not-allowed resize-none text-sm md:text-base"
        style={{ maxHeight: '120px' }}
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="bg-gradient-to-br from-primary to-accent hover:from-primary/90 hover:to-accent/90 disabled:opacity-50 disabled:cursor-not-allowed text-card px-4 md:px-5 py-3 rounded-xl font-medium transition-all flex items-center gap-2 flex-shrink-0 text-sm md:text-base"
      >
        <span className="hidden sm:inline">Send</span>
        <Send size={18} />
      </button>
    </form>
  )
}
