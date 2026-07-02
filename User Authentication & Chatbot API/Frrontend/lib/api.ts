// API client for the chat backend.
// Configure the base URL with NEXT_PUBLIC_API_URL, defaults to http://localhost:8000.

export const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "http://localhost:8000"

const TOKEN_KEY = "chat_token"
const USER_KEY = "chat_user"

export type StoredUser = {
  id?: string | number
  full_name?: string
  email?: string
}

export type ChatMessage = {
  id: string
  role: "user" | "bot"
  content: string
  createdAt?: string
}

export type Conversation = {
  id: string
  title: string
  messages: ChatMessage[]
}

/* ---------------- token helpers ---------------- */

export function getToken(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getStoredUser(): StoredUser | null {
  if (typeof window === "undefined") return null
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as StoredUser
  } catch {
    return null
  }
}

export function setStoredUser(user: StoredUser) {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

/* ---------------- request helper ---------------- */

async function request<T>(
  path: string,
  options: RequestInit = {},
  withAuth = false,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  }

  if (withAuth) {
    const token = getToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  let res: Response
  try {
    res = await fetch(`${API_URL}${path}`, { ...options, headers })
  } catch {
    throw new Error(
      `Could not reach the server at ${API_URL}. Make sure your backend is running.`,
    )
  }

  let data: unknown = null
  const text = await res.text()
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = text
    }
  }

  if (!res.ok) {
    const detail =
      (data as { detail?: string; message?: string })?.detail ||
      (data as { message?: string })?.message ||
      (typeof data === "string" ? data : "") ||
      `Request failed (${res.status})`
    throw new Error(detail)
  }

  return data as T
}

/* ---------------- endpoints ---------------- */

export async function signup(payload: {
  full_name: string
  email: string
  password: string
}) {
  return request<Record<string, unknown>>("/signup", {
    method: "POST",
    body: JSON.stringify(payload),
  })
}

export async function login(payload: { email: string; password: string }) {
  const data = await request<Record<string, unknown>>("/login", {
    method: "POST",
    body: JSON.stringify(payload),
  })

  const token =
    (data.access_token as string) ||
    (data.token as string) ||
    (data.jwt as string)
  if (token) setToken(token)

  const user =
    (data.user as StoredUser) ||
    ({
      id: data.user_id as string | number | undefined,
      email: (data.email as string) || payload.email,
      full_name: data.full_name as string | undefined,
    } as StoredUser)
  setStoredUser(user)

  return { token, user, raw: data }
}

export async function sendMessage(message: string) {
  const data = await request<Record<string, unknown>>(
    "/chat/",
    {
      method: "POST",
      body: JSON.stringify({ message }),
    },
    true,
  )

  const reply =
    (data.bot_response as string) ||      // ← YOUR BACKEND RETURNS THIS
    (data.response as string) ||
    (data.reply as string) ||
    (data.message as string) ||
    (data.answer as string) ||
    (typeof data === "string" ? data : "")

  return {
    reply,
    userId: (data.user_id as string) ?? undefined,
    botId: (data.bot_id as string) ?? undefined,
    raw: data,
  }
}

export async function getHistory(): Promise<ChatMessage[]> {
  const data = await request<unknown>("/chat/history", { method: "GET" }, true)

  const list = Array.isArray(data)
    ? data
    : ((data as { history?: unknown[]; messages?: unknown[] })?.history ??
      (data as { messages?: unknown[] })?.messages ??
      [])

  const messages: ChatMessage[] = []
  ;(list as Record<string, unknown>[]).forEach((item, i) => {
    // A history item may be a single message or a {message, response} pair.
    const userText =
      (item.message as string) ??
      (item.prompt as string) ??
      (item.question as string)
    const botText =
      (item.response as string) ??
      (item.reply as string) ??
      (item.answer as string)

    if (userText !== undefined || botText !== undefined) {
      if (userText)
        messages.push({
          id: `${i}-u`,
          role: "user",
          content: userText,
          createdAt: item.created_at as string | undefined,
        })
      if (botText)
        messages.push({
          id: `${i}-b`,
          role: "bot",
          content: botText,
          createdAt: item.created_at as string | undefined,
        })
    } else if (item.role && item.content) {
      messages.push({
        id: (item.id as string) ?? `${i}`,
        role: item.role === "user" ? "user" : "bot",
        content: item.content as string,
        createdAt: item.created_at as string | undefined,
      })
    }
  })

  return messages
}
