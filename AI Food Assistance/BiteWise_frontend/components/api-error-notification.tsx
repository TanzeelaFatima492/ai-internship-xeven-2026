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

/**
 * Component to display API error/warning/info notifications
 */
export default function ApiErrorNotification({
  message,
  type = 'error',
  status,
  onClose,
  autoClose = true,
  autoCloseDelay = 5000,
}: ApiErrorNotificationProps) {
  const [isVisible, setIsVisible] = useState(!!message)

  useEffect(() => {
    setIsVisible(!!message)

    if (message && autoClose) {
      const timer = setTimeout(() => {
        setIsVisible(false)
        onClose?.()
      }, autoCloseDelay)

      return () => clearTimeout(timer)
    }
  }, [message, autoClose, autoCloseDelay, onClose])

  const handleClose = () => {
    setIsVisible(false)
    onClose?.()
  }

  if (!isVisible || !message) {
    return null
  }

  const baseClasses =
    'flex items-start gap-3 p-4 rounded-lg border mb-4 animate-in fade-in slide-in-from-top-2 duration-200'

  const typeClasses = {
    error: 'bg-destructive/10 border-destructive/30 text-destructive',
    warning: 'bg-amber-500/10 border-amber-500/30 text-amber-600',
    info: 'bg-blue-500/10 border-blue-500/30 text-blue-600',
  }

  const iconClasses = {
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
  }

  const Icon = iconClasses[type]

  return (
    <div className={`${baseClasses} ${typeClasses[type]}`} role="alert">
      <Icon className="flex-shrink-0 w-5 h-5 mt-0.5" />
      <div className="flex-1">
        <p className="font-medium">{message}</p>
        {status && (
          <p className="text-sm opacity-75 mt-1">
            Status code: {status}
          </p>
        )}
      </div>
      <button
        onClick={handleClose}
        className="flex-shrink-0 p-1 hover:bg-current/20 rounded transition-colors"
        aria-label="Close notification"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}
