"use client"

import { useEffect, useState } from "react"
import { AlertCircle, Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { ChatSidebar } from "@/components/chat-sidebar"
import { ChatMessages } from "@/components/chat-messages"
import { MessageInput } from "@/components/message-input"
import {
  getHistory,
  sendMessage,
  type ChatMessage,
  type Conversation,
  type StoredUser,
} from "@/lib/api"

let idCounter = 0
const nextId = () => `local-${Date.now()}-${idCounter++}`

export function ChatView({
  user,
  onLogout,
}: {
  user: StoredUser | null
  onLogout: () => void
}) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)
  const [loadingHistory, setLoadingHistory] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const [userId, setUserId] = useState<string>(
    user?.id !== undefined ? String(user.id) : "—",
  )
  
  const [botId, setBotId] = useState<number>(() => {
    if (typeof window !== "undefined" && user?.id) {
      const saved = localStorage.getItem(`chat_bot_id_${user.id}`)
      return saved ? Number(saved) : 0
    }
    return 0
  })

  const active = conversations.find((c) => c.id === activeId) ?? null

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoadingHistory(true)
      try {
        const history = await getHistory()
        if (cancelled) return
        
        if (history.length > 0) {
          const groupedByBot: Record<string, ChatMessage[]> = {}
          history.forEach((msg: any) => {
            const bId = msg.bot_id ? String(msg.bot_id) : "default"
            if (!groupedByBot[bId]) groupedByBot[bId] = []
            groupedByBot[bId].push(msg)
          })
          
          const convos: Conversation[] = Object.entries(groupedByBot).map(([bId, msgs]) => ({
            id: bId,
            title: deriveTitle(msgs),
            messages: msgs.reverse(),
          }))
          
          setConversations(convos)
          setActiveId(convos[0]?.id || null)

          console.log("Total convos:", convos.length)
          console.log("Convo titles:", convos.map(c => c.title))
          console.log("Convo IDs:", convos.map(c => c.id))
          
          const firstBotId = Object.keys(groupedByBot)[0]
          if (firstBotId && firstBotId !== "default") {
            setBotId(Number(firstBotId))
            localStorage.setItem(`chat_bot_id_${user?.id}`, firstBotId)
          }
        } else {
          startNewChat()
        }
      } catch (err) {
        if (cancelled) return
        setError(err instanceof Error ? err.message : "Failed to load chat history.")
        startNewChat()
      } finally {
        if (!cancelled) setLoadingHistory(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  function startNewChat() {
    const convo: Conversation = {
      id: nextId(),
      title: "New chat",
      messages: [],
    }
    setConversations((prev) => {
      const withoutEmpty = prev.filter((c) => c.messages.length > 0)
      return [convo, ...withoutEmpty]
    })
    setActiveId(convo.id)
    setBotId(0)
    localStorage.removeItem(`chat_bot_id_${userId}`)
    setSidebarOpen(false)
  }

  function updateConversation(id: string, updater: (c: Conversation) => Conversation) {
    setConversations((prev) => prev.map((c) => (c.id === id ? updater(c) : c)))
  }

  async function handleSend(text: string) {
    setError(null)
    let convoId = activeId
    
    // ✅ New conversation when botId is 0 (fresh start)
    if (!convoId || botId === 0) {
      const convo: Conversation = { id: nextId(), title: text.slice(0, 32), messages: [] }
      setConversations((prev) => [convo, ...prev])
      setActiveId(convo.id)
      convoId = convo.id
    }

    const userMsg: ChatMessage = {
      id: nextId(),
      role: "user",
      content: text,
    }

    updateConversation(convoId, (c) => ({
      ...c,
      title: c.messages.length === 0 ? (text.length > 32 ? text.slice(0, 32) + "…" : text) : c.title,
      messages: [...c.messages, userMsg],
    }))

    setSending(true)
    try {
      const { response, userId: uid, botId: bid } = await sendMessage(text, botId)
      if (uid) setUserId(String(uid))
      
      if (bid && bid !== 0) {
        setBotId(bid)
        localStorage.setItem(`chat_bot_id_${uid}`, String(bid))
      }

      const botMsg: ChatMessage = {
        id: nextId(),
        role: "bot",
        content: response || "(no response)",
      }

      updateConversation(convoId, (c) => ({
        ...c,
        messages: [...c.messages, botMsg],
      }))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message")
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="flex h-dvh overflow-hidden bg-background">
      <ChatSidebar
        open={sidebarOpen}
        conversations={conversations}
        activeId={activeId}
        user={user}
        onSelect={(id) => {
          setActiveId(id)
          const convo = conversations.find(c => c.id === id)
          if (convo && !convo.id.startsWith("local-")) {
            setBotId(Number(convo.id))
            localStorage.setItem(`chat_bot_id_${userId}`, convo.id)
          }
          setSidebarOpen(false)
        }}
        onNewChat={startNewChat}
        onLogout={onLogout}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
          <div className="flex min-w-0 items-center gap-2">
            <Button
              variant="ghost"
              size="icon-sm"
              className="md:hidden"
              onClick={() => setSidebarOpen(true)}
              aria-label="Open sidebar"
            >
              <Menu className="size-5" />
            </Button>
            <h1 className="truncate font-heading text-base font-semibold">
              {active?.title ?? "Chat"}
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 text-xs sm:flex">
              <IdPill label="User" value={userId} />
              <IdPill label="Bot" value={String(botId)} />
            </div>
            <ThemeToggle />
          </div>
        </header>

        {error && (
          <div
            role="alert"
            className="flex items-start gap-2 border-b border-destructive/20 bg-destructive/10 px-4 py-2 text-sm text-destructive"
          >
            <AlertCircle className="mt-0.5 size-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <ChatMessages
          messages={active?.messages ?? []}
          loading={loadingHistory}
          pending={sending}
        />

        <MessageInput onSend={handleSend} disabled={sending} />
      </div>
    </div>
  )
}

function IdPill({ label, value }: { label: string; value: string }) {
  return (
    <span className="flex items-center gap-1 rounded-full bg-muted px-2.5 py-1 font-mono text-xs text-muted-foreground">
      <span className="text-[0.65rem] font-medium uppercase tracking-wide opacity-70">
        {label}
      </span>
      <span className="max-w-24 truncate text-foreground">{value}</span>
    </span>
  )
}

function deriveTitle(messages: ChatMessage[]): string {
  const first = messages.find((m) => m.role === "user") ?? messages[0]
  if (!first) return "New chat"
  return first.content.length > 32
    ? `${first.content.slice(0, 32)}…`
    : first.content
}