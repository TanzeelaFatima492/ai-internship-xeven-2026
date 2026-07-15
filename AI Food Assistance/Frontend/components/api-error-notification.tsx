import { AlertCircle, AlertTriangle, Info, X } from 'lucide-react'
import { useEffect, useState } from 'react'

export interface ApiErrorNotificationProps {
  message: string | null
  type?: 'error' | 'warning' | 'info'
  status?: number | null
  onClose?: () => void
  autoClose?: boolean
  autoCloseDelay?: number
}

export default function ApiErrorNotification({
  message, type = 'error', status, onClose, autoClose = true, autoCloseDelay = 5000,
}: ApiErrorNotificationProps) {
  const [isVisible, setIsVisible] = useState(!!message)

  useEffect(() => {
    setIsVisible(!!message)
    if (message && autoClose) {
      const timer = setTimeout(() => { setIsVisible(false); onClose?.() }, autoCloseDelay)
      return () => clearTimeout(timer)
    }
  }, [message, autoClose, autoCloseDelay, onClose])

  if (!isVisible || !message) return null

  const typeClasses = {
    error: 'bg-red-500/10 border-red-500/30 text-red-400',
    warning: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
    info: 'bg-orange-500/10 border-orange-500/30 text-orange-400',
  }

  const icons = { error: AlertCircle, warning: AlertTriangle, info: Info }
  const Icon = icons[type]

  return (
    <div className={`flex items-start gap-3 p-4 rounded-lg border mb-4 ${typeClasses[type]}`} role="alert">
      <Icon className="flex-shrink-0 w-5 h-5 mt-0.5" />
      <div className="flex-1">
        <p className="font-medium">{message}</p>
        {status && <p className="text-sm opacity-75 mt-1">Status: {status}</p>}
      </div>
      <button onClick={() => { setIsVisible(false); onClose?.() }} className="p-1 hover:bg-white/10 rounded">
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}