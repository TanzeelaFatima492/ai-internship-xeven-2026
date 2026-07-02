"use client"

import type React from "react"
import { useRef, useState } from "react"
import { SendHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"

export function MessageInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void
  disabled: boolean
}) {
  const [value, setValue] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  function submit() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue("")
    if (textareaRef.current) textareaRef.current.style.height = "auto"
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (
      e.key === "Enter" &&
      !e.shiftKey &&
      !e.nativeEvent.isComposing &&
      e.keyCode !== 229
    ) {
      e.preventDefault()
      submit()
    }
  }

  function handleInput(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setValue(e.target.value)
    const el = e.target
    el.style.height = "auto"
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`
  }

  return (
    <div className="border-t border-border bg-background px-4 py-3">
      <div className="mx-auto flex max-w-3xl items-end gap-2">
        <div className="flex flex-1 items-end rounded-2xl border border-input bg-muted/40 px-3 py-2 focus-within:border-ring focus-within:ring-3 focus-within:ring-ring/50">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder="Type a message..."
            className="max-h-40 flex-1 resize-none bg-transparent text-sm leading-relaxed outline-none placeholder:text-muted-foreground"
          />
        </div>
        <Button
          onClick={submit}
          disabled={disabled || !value.trim()}
          size="icon-lg"
          className="size-11 shrink-0 rounded-full"
          aria-label="Send message"
        >
          <SendHorizontal className="size-5" />
        </Button>
      </div>
    </div>
  )
}
