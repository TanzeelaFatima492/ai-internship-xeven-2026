"use client"

import { LogOut, MessageSquare, Plus, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { Conversation, StoredUser } from "@/lib/api"

export function ChatSidebar({
  open,
  conversations,
  activeId,
  user,
  onSelect,
  onNewChat,
  onLogout,
  onClose,
}: {
  open: boolean
  conversations: Conversation[]
  activeId: string | null
  user: StoredUser | null
  onSelect: (id: string) => void
  onNewChat: () => void
  onLogout: () => void
  onClose: () => void
}) {
  const initials =
    user?.full_name
      ?.split(" ")
      .map((p) => p[0])
      .slice(0, 2)
      .join("")
      .toUpperCase() ||
    user?.email?.[0]?.toUpperCase() ||
    "U"

  return (
    <>
      {open && (
        <div
          className="fixed inset-0 z-30 bg-foreground/40 md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-sidebar-border bg-sidebar transition-transform duration-200 md:static md:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between px-4 py-4">
          <div className="flex items-center gap-2">
            <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <MessageSquare className="size-4" />
            </div>
            <span className="font-heading text-base font-semibold text-sidebar-foreground">
              Pulse Chat
            </span>
          </div>
          <Button
            variant="ghost"
            size="icon-sm"
            className="md:hidden"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <X className="size-4" />
          </Button>
        </div>

        <div className="px-3">
          <Button
            onClick={onNewChat}
            variant="outline"
            className="h-10 w-full justify-start gap-2 text-sm"
          >
            <Plus className="size-4" />
            New chat
          </Button>
        </div>

        <nav className="mt-4 flex-1 overflow-y-auto px-3 pb-4">
          <p className="px-2 py-2 text-xs font-medium text-muted-foreground">
            Recent
          </p>
          {conversations.length === 0 ? (
            <p className="px-2 py-2 text-sm text-muted-foreground">
              No conversations yet.
            </p>
          ) : (
            <ul className="flex flex-col gap-1">
              {conversations.map((c) => (
                <li key={c.id}>
                  <button
                    onClick={() => onSelect(c.id)}
                    className={`flex w-full items-center gap-2 truncate rounded-lg px-2 py-2 text-left text-sm transition-colors ${
                      activeId === c.id
                        ? "bg-sidebar-accent text-sidebar-accent-foreground"
                        : "text-sidebar-foreground/80 hover:bg-sidebar-accent/60"
                    }`}
                  >
                    <MessageSquare className="size-4 shrink-0 text-muted-foreground" />
                    <span className="truncate">{c.title}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </nav>

        <div className="border-t border-sidebar-border p-3">
          <div className="flex items-center gap-3">
            <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
              {initials}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-sidebar-foreground">
                {user?.full_name || "User"}
              </p>
              <p className="truncate text-xs text-muted-foreground">
                {user?.email}
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon-sm"
              onClick={onLogout}
              aria-label="Log out"
              className="text-muted-foreground hover:text-foreground"
            >
              <LogOut className="size-4" />
            </Button>
          </div>
        </div>
      </aside>
    </>
  )
}
