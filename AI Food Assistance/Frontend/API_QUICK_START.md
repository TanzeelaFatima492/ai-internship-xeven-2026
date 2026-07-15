# API Client - Quick Start Guide

## 1. Setup Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_STORAGE_KEY=bitewise_auth_token
NEXT_PUBLIC_API_TIMEOUT=30000
NEXT_PUBLIC_API_DEBUG=false
```

## 2. Basic Usage in Components

### GET Request

```typescript
import { apiGet } from '@/lib/api-client'

const menu = await apiGet('/api/menu')
```

### POST Request

```typescript
import { apiPost } from '@/lib/api-client'

const response = await apiPost('/api/chat', {
  message: 'Hello',
})
```

### PUT/PATCH Request

```typescript
import { apiPut, apiPatch } from '@/lib/api-client'

await apiPut('/api/document/1', { name: 'Menu' })
await apiPatch('/api/document/1', { status: 'active' })
```

### DELETE Request

```typescript
import { apiDelete } from '@/lib/api-client'

await apiDelete('/api/document/1')
```

## 3. Using the useApi Hook (Recommended)

```typescript
'use client'

import { useApi } from '@/hooks/use-api'

export function MyComponent() {
  const { get, post, data, loading, error } = useApi()

  const loadData = async () => {
    await get('/api/menu')
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      <button onClick={loadData}>Load</button>
    </div>
  )
}
```

## 4. Error Handling

```typescript
import { useApiError } from '@/hooks/use-api-error'
import ApiErrorNotification from '@/components/api-error-notification'

export function MyComponent() {
  const { error, handleError, clearError } = useApiError()

  const handleFetch = async () => {
    try {
      await apiGet('/api/menu')
    } catch (err) {
      handleError(err)
    }
  }

  return (
    <>
      <ApiErrorNotification
        message={error.message}
        type={error.type}
        status={error.status}
        onClose={clearError}
      />
      <button onClick={handleFetch}>Fetch</button>
    </>
  )
}
```

## 5. JWT Token Management

```typescript
import {
  getAuthToken,
  setAuthToken,
  clearAuthToken,
} from '@/lib/api-client'

// After successful login
setAuthToken(response.token)

// Get current token
const token = getAuthToken()

// On logout
clearAuthToken()
```

## 6. Error Status Codes

| Status | Handling | User Message |
|--------|----------|--------------|
| 401 | Auto-redirect to login | Session expired |
| 429 | Show warning | Too many requests |
| 400 | Show error | Invalid request |
| 404 | Show error | Not found |
| 500+ | Show error | Server error |
| 0 | Show error | Network error |

## 7. Custom Request Options

```typescript
import { apiGet, type ApiRequestOptions } from '@/lib/api-client'

const options: ApiRequestOptions = {
  timeout: 60000,        // Custom timeout
  skipAuth: false,       // Skip JWT token
  headers: {             // Additional headers
    'X-Custom': 'value',
  },
}

await apiGet('/api/menu', options)
```

## 8. Debug Mode

Enable in `.env.local`:

```bash
NEXT_PUBLIC_API_DEBUG=true
```

Then check browser console for API logs.

## 9. File Upload

```typescript
const formData = new FormData()
formData.append('file', file)
formData.append('name', 'Menu')

await apiPost('/api/upload', formData, {
  headers: {} as HeadersInit,
})
```

## 10. TypeScript Support

```typescript
interface MenuItem {
  id: number
  name: string
  price: number
}

const menu = await apiGet<MenuItem[]>('/api/menu')
// menu is properly typed as MenuItem[]
```

## Common Patterns

### Request with Loading State

```typescript
const { get, loading } = useApi()

return (
  <button onClick={() => get('/api/menu')} disabled={loading}>
    {loading ? 'Loading...' : 'Fetch Menu'}
  </button>
)
```

### Request with Error Display

```typescript
const { post, error } = useApi()

return (
  <>
    {error && <div className="text-red-500">{error}</div>}
    <button onClick={() => post('/api/chat', { msg: 'hello' })}>
      Send
    </button>
  </>
)
```

### Request with Success Callback

```typescript
const { get } = useApi()

const loadMenu = async () => {
  try {
    const data = await get('/api/menu')
    console.log('Menu loaded:', data)
    // Update state, show success, etc.
  } catch (err) {
    console.error('Failed:', err)
  }
}
```

## Files Created

- `/lib/api-client.ts` - Core API client
- `/hooks/use-api.ts` - React hook for API calls
- `/hooks/use-api-error.ts` - Error handling hook
- `/components/api-error-notification.tsx` - Error display
- `/components/api-example.tsx` - Example component
- `.env.example` - Environment template
- `.env.development.local` - Development config

## Next Steps

1. Configure `.env.local` with your FastAPI URL
2. Test with the example component
3. Integrate into your app components
4. Set up backend CORS if needed
5. Deploy with production environment variables

For detailed documentation, see `API_SETUP.md`.
