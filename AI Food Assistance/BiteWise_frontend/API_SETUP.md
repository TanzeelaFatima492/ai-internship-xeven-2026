# FastAPI Backend Integration Guide

## Overview

This document describes the frontend configuration for connecting to a FastAPI backend with JWT authentication, error handling, and rate limiting support.

## Environment Variables

Create a `.env.local` file in the project root with the following configuration:

```bash
# FastAPI Backend Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# JWT Token Configuration
NEXT_PUBLIC_JWT_STORAGE_KEY=bitewise_auth_token

# API Request Configuration
NEXT_PUBLIC_API_TIMEOUT=30000        # Timeout in milliseconds
NEXT_PUBLIC_API_DEBUG=false          # Enable API request logging
```

### Environment Variables Explanation

- `NEXT_PUBLIC_API_BASE_URL`: The base URL of your FastAPI backend (e.g., http://localhost:8000)
- `NEXT_PUBLIC_JWT_STORAGE_KEY`: Key name for storing JWT token in localStorage
- `NEXT_PUBLIC_API_TIMEOUT`: Request timeout duration in milliseconds (default: 30000ms)
- `NEXT_PUBLIC_API_DEBUG`: Enable console logging for all API requests/responses

> **Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the client-side JavaScript

## API Client Usage

### Basic API Calls

The API client provides simple methods for common HTTP operations:

#### GET Request

```typescript
import { apiGet } from '@/lib/api-client'

const data = await apiGet<MenuData>('/api/menu')
```

#### POST Request

```typescript
import { apiPost } from '@/lib/api-client'

const response = await apiPost('/api/chat', {
  message: 'What are your vegetarian options?'
})
```

#### PUT/PATCH Request

```typescript
import { apiPut, apiPatch } from '@/lib/api-client'

await apiPut('/api/documents/1', { name: 'Updated Menu' })
await apiPatch('/api/documents/1', { status: 'active' })
```

#### DELETE Request

```typescript
import { apiDelete } from '@/lib/api-client'

await apiDelete('/api/documents/1')
```

### JWT Token Management

The API client automatically manages JWT tokens:

```typescript
import {
  getAuthToken,
  setAuthToken,
  clearAuthToken,
} from '@/lib/api-client'

// Get current token
const token = getAuthToken()

// Set token (after login)
setAuthToken(newToken)

// Clear token (on logout)
clearAuthToken()
```

## Error Handling

### Automatic Error Handling

The API client handles errors automatically:

- **401 Unauthorized**: Clears token and redirects to login page
- **429 Too Many Requests**: Shows "Too many requests" message
- **Network Errors**: Shows connection error message
- **Timeout Errors**: Shows timeout message

### Using the useApi Hook

For components, use the `useApi` hook with built-in loading and error states:

```typescript
'use client'

import { useApi } from '@/hooks/use-api'
import { useApiError } from '@/hooks/use-api-error'
import ApiErrorNotification from '@/components/api-error-notification'

export function MenuComponent() {
  const { get, data, loading, error } = useApi<MenuItem[]>()
  const { error: apiError, clearError } = useApiError()

  const loadMenu = async () => {
    try {
      await get('/api/menu')
    } catch (err) {
      console.error('Failed to load menu:', err)
    }
  }

  return (
    <div>
      <ApiErrorNotification
        message={apiError.message}
        type={apiError.type || 'error'}
        status={apiError.status}
        onClose={clearError}
      />

      <button onClick={loadMenu} disabled={loading}>
        {loading ? 'Loading...' : 'Load Menu'}
      </button>

      {data && (
        <ul>
          {data.map((item) => (
            <li key={item.id}>{item.name} - ${item.price}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
```

### Manual Error Handling

For more control, catch and handle errors manually:

```typescript
import { apiGet, ApiError } from '@/lib/api-client'
import { useApiError } from '@/hooks/use-api-error'

export function ChatComponent() {
  const { handleError } = useApiError()

  const sendMessage = async (message: string) => {
    try {
      const response = await apiGet('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ message }),
      })
      console.log('Response:', response)
    } catch (err) {
      handleError(err)
      // Error is automatically categorized and displayed
    }
  }

  return <button onClick={() => sendMessage('Hello')}>Send</button>
}
```

### ApiErrorNotification Component

Display errors to users with the built-in notification component:

```typescript
import ApiErrorNotification from '@/components/api-error-notification'
import { useState } from 'react'

export function MyComponent() {
  const [error, setError] = useState<string | null>(null)

  return (
    <>
      <ApiErrorNotification
        message={error}
        type="error"
        onClose={() => setError(null)}
        autoClose={true}
        autoCloseDelay={5000}
      />

      {/* Your component content */}
    </>
  )
}
```

## Request Options

All API methods accept optional configuration:

```typescript
import { apiGet, type ApiRequestOptions } from '@/lib/api-client'

const options: ApiRequestOptions = {
  timeout: 60000,           // Custom timeout (ms)
  skipAuth: false,          // Skip JWT token attachment
  headers: {                // Additional headers
    'X-Custom-Header': 'value',
  },
}

const data = await apiGet('/api/menu', options)
```

## Error Types

### ApiError

All API errors throw an `ApiError` instance with:

```typescript
class ApiError {
  message: string      // Human-readable error message
  status: number       // HTTP status code
  data?: unknown       // Response data (if available)
}
```

## Common Scenarios

### Login/Signup Flow

```typescript
// After successful authentication from login page
import { setAuthToken } from '@/lib/api-client'

setAuthToken(response.token)
// User is now authenticated for all subsequent requests
```

### Rate Limiting

The API client automatically detects 429 responses:

```typescript
try {
  await apiPost('/api/chat', { message: 'Hello' })
} catch (err) {
  if (err instanceof ApiError && err.status === 429) {
    // Show rate limit message and retry later
    console.log('Rate limited. Try again in 1 minute.')
  }
}
```

### Session Expiration

If JWT token expires (401 response), the client automatically:
1. Clears the token
2. Redirects to login page
3. Shows authentication error

### File Upload

For multipart/form-data requests:

```typescript
const formData = new FormData()
formData.append('file', pdfFile)
formData.append('name', 'Menu')

await apiPost('/api/documents/upload', formData, {
  headers: {
    // Remove Content-Type header to let browser set it with boundary
  } as HeadersInit,
})
```

## API Debug Mode

Enable debug logging for development:

```bash
NEXT_PUBLIC_API_DEBUG=true
```

This will log all API requests and responses to the console:

```javascript
[API] Request: {
  url: "http://localhost:8000/api/menu",
  method: "GET",
  headers: { Authorization: "Bearer ..." }
}

[API] Response: {
  status: 200,
  data: [{ id: 1, name: "Biryani" }]
}
```

## Best Practices

1. **Always handle errors**: Use error notifications or fallback UI
2. **Show loading states**: Disable buttons and show spinners during requests
3. **Use typed responses**: Specify response types for better TypeScript support
4. **Avoid token exposure**: Never log or send tokens in non-secure contexts
5. **Request deduplication**: Prevent duplicate requests while one is in flight
6. **Cache responses**: Use SWR or similar for frequently accessed data

## Troubleshooting

### Token not persisting

- Check that localStorage is enabled in browser
- Verify `NEXT_PUBLIC_JWT_STORAGE_KEY` is set correctly
- Ensure token is set after login: `setAuthToken(token)`

### 401 errors on valid token

- Verify token format is correct (JWT with Bearer prefix)
- Check token expiration on backend
- Ensure Authorization header is properly formatted

### 429 rate limit errors

- Add delay between requests
- Implement exponential backoff retry logic
- Check backend rate limit configuration

### Network timeouts

- Increase `NEXT_PUBLIC_API_TIMEOUT` if requests are slow
- Check backend server is running
- Verify `NEXT_PUBLIC_API_BASE_URL` is correct

## Backend CORS Configuration

Your FastAPI backend must allow requests from your frontend URL. Example:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Support for Multiple Environments

Create separate environment files:

```bash
.env.local              # Local development
.env.development        # Development server
.env.staging           # Staging environment
.env.production        # Production environment
```

Each file can have different API URLs and configurations.

## Related Files

- `/lib/api-client.ts` - Core API client implementation
- `/hooks/use-api.ts` - React hook for API calls
- `/hooks/use-api-error.ts` - Error handling hook
- `/components/api-error-notification.tsx` - Error notification component
