# FastAPI Backend Integration - Complete Setup

## Overview

A comprehensive frontend configuration has been created for seamless integration with a FastAPI backend. The setup includes JWT authentication, automatic error handling, rate limiting support, and a robust API client with React hooks.

## What Was Created

### 1. Environment Configuration

**Files Created:**
- `.env.example` - Template for environment variables
- `.env.development.local` - Development configuration (updated)

**Key Environment Variables:**
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_STORAGE_KEY=bitewise_auth_token
NEXT_PUBLIC_API_TIMEOUT=30000
NEXT_PUBLIC_API_DEBUG=false
```

### 2. Core API Client

**File:** `/lib/api-client.ts` (259 lines)

Features:
- Automatic JWT token attachment to all requests
- Support for GET, POST, PUT, PATCH, DELETE methods
- Global error handling (401, 429, network errors, timeouts)
- Request/response logging in debug mode
- Type-safe API calls with TypeScript generics
- Configurable request timeouts

**Key Functions:**
```typescript
apiGet<T>(endpoint, options)      // GET request
apiPost<T>(endpoint, data, options) // POST request
apiPut<T>(endpoint, data, options)  // PUT request
apiPatch<T>(endpoint, data, options) // PATCH request
apiDelete<T>(endpoint, options)   // DELETE request

getAuthToken()                     // Get stored JWT
setAuthToken(token)               // Store JWT
clearAuthToken()                  // Remove JWT
```

### 3. React Hooks

**File 1:** `/hooks/use-api.ts` (97 lines)

Provides hooks for making API calls with automatic state management:
```typescript
const { get, post, put, patch, delete, data, loading, error } = useApi<T>()
```

Features:
- Automatic loading/error states
- Request execution with callbacks
- Type-safe response data

**File 2:** `/hooks/use-api-error.ts` (121 lines)

Handles API errors with user-friendly categorization:
```typescript
const { error, handleError, clearError, hasError } = useApiError()
```

Features:
- Status code categorization
- Error type classification (error, warning, info)
- User-friendly error messages
- Automatic session expiration handling

### 4. UI Components

**File 1:** `/components/api-error-notification.tsx` (86 lines)

Displays error notifications to users:
```tsx
<ApiErrorNotification
  message={error.message}
  type="error"
  status={error.status}
  onClose={handleClose}
  autoClose={true}
  autoCloseDelay={5000}
/>
```

Features:
- Color-coded notifications (error/warning/info)
- Auto-dismiss after delay
- Manual close button
- Icon indicators

**File 2:** `/components/api-example.tsx` (194 lines)

Example component demonstrating all API patterns:
- GET request example
- POST request example
- Rate limiting handling
- Response display
- Configuration info display

### 5. Documentation

**API_SETUP.md** (383 lines)
- Complete integration guide
- Detailed error handling patterns
- Best practices and troubleshooting
- Backend CORS configuration
- Multi-environment setup

**API_QUICK_START.md** (253 lines)
- Quick reference guide
- Common patterns
- Status code handling table
- File upload instructions
- TypeScript support examples

## Error Handling Specification

### Automatic Error Handling

| Error | Auto-Handle | User Message | Action |
|-------|-------------|--------------|--------|
| **401 Unauthorized** | ✓ | "Your session has expired. Please log in again." | Redirect to login |
| **429 Too Many Requests** | ✓ | "Too many requests. Please wait a moment and try again." | Show warning |
| **400 Bad Request** | ✓ | "Invalid request. Please check your input." | Show error |
| **404 Not Found** | ✓ | "Resource not found." | Show error |
| **500+ Server Errors** | ✓ | "Server error. Please try again later." | Show error |
| **Network Error** | ✓ | "Network error. Please check your connection." | Show error |
| **Request Timeout** | ✓ | "Request timeout after 30000ms" | Show error |

### 401 Unauthorized Flow

When 401 error occurs:
1. JWT token is automatically cleared from localStorage
2. User is redirected to login page
3. Error notification is shown to user
4. Next API call will skip auth headers until new token is set

### 429 Rate Limiting Flow

When 429 error occurs:
1. User-friendly warning message is displayed
2. Request is not retried automatically
3. User can implement manual retry with exponential backoff
4. UI remains interactive for manual retry

## JWT Token Management

### Setting Token (After Login)

```typescript
import { setAuthToken } from '@/lib/api-client'

// After successful login
const response = await apiPost('/api/auth/login', { username, password })
setAuthToken(response.token)
// Token now attached to all subsequent requests
```

### Getting Token

```typescript
import { getAuthToken } from '@/lib/api-client'

const token = getAuthToken()
if (token) {
  console.log('User is authenticated')
}
```

### Clearing Token (On Logout)

```typescript
import { clearAuthToken } from '@/lib/api-client'

clearAuthToken()
// Next requests will not include Authorization header
```

## Integration Patterns

### Pattern 1: Simple API Call

```typescript
import { apiGet } from '@/lib/api-client'

const menu = await apiGet('/api/menu')
```

### Pattern 2: With Loading State

```typescript
'use client'
import { useApi } from '@/hooks/use-api'

export function MenuComponent() {
  const { get, loading } = useApi()
  
  return (
    <button onClick={() => get('/api/menu')} disabled={loading}>
      {loading ? 'Loading...' : 'Load Menu'}
    </button>
  )
}
```

### Pattern 3: With Error Handling

```typescript
'use client'
import { useApiError } from '@/hooks/use-api-error'
import ApiErrorNotification from '@/components/api-error-notification'

export function ChatComponent() {
  const { error, handleError, clearError } = useApiError()
  
  const sendMessage = async (message: string) => {
    try {
      await apiPost('/api/chat', { message })
    } catch (err) {
      handleError(err)
    }
  }
  
  return (
    <>
      <ApiErrorNotification
        message={error.message}
        type={error.type}
        onClose={clearError}
      />
      <button onClick={() => sendMessage('Hello')}>Send</button>
    </>
  )
}
```

### Pattern 4: Complete Implementation

```typescript
'use client'
import { useApi } from '@/hooks/use-api'
import { useApiError } from '@/hooks/use-api-error'
import ApiErrorNotification from '@/components/api-error-notification'

export function CompleteComponent() {
  const { post, data, loading } = useApi()
  const { error, handleError, clearError } = useApiError()

  const handleSubmit = async (text: string) => {
    try {
      await post('/api/chat', { message: text })
    } catch (err) {
      handleError(err)
    }
  }

  return (
    <>
      <ApiErrorNotification
        message={error.message}
        type={error.type}
        onClose={clearError}
      />
      <form onSubmit={(e) => {
        e.preventDefault()
        handleSubmit(e.target.message.value)
      }}>
        <input name="message" />
        <button disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
      {data && <div>{JSON.stringify(data)}</div>}
    </>
  )
}
```

## Backend Requirements

### CORS Configuration

Your FastAPI backend must enable CORS for your frontend URL:

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

### JWT Bearer Token

Backend should accept JWT in Authorization header:

```
Authorization: Bearer <token>
```

### Error Response Format

Backend should return proper status codes:
- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Invalid/expired token
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limited
- `500 Internal Server Error` - Server error

Optional JSON response body:
```json
{
  "message": "Error description",
  "error": "Error type",
  "data": {}
}
```

## Configuration for Different Environments

### Development

```bash
# .env.development.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_DEBUG=true
```

### Staging

```bash
# .env.staging
NEXT_PUBLIC_API_BASE_URL=https://api-staging.example.com
NEXT_PUBLIC_API_DEBUG=false
```

### Production

```bash
# .env.production
NEXT_PUBLIC_API_BASE_URL=https://api.example.com
NEXT_PUBLIC_API_DEBUG=false
```

## Testing the Setup

### 1. Verify Environment Variables

```bash
cat .env.development.local
# Should show API_BASE_URL configuration
```

### 2. Run Development Server

```bash
pnpm dev
# Server starts at http://localhost:3000
```

### 3. Test API Calls

Use the provided example component:
```tsx
import ApiExample from '@/components/api-example'

export default function TestPage() {
  return <ApiExample />
}
```

### 4. Enable Debug Mode

```bash
NEXT_PUBLIC_API_DEBUG=true pnpm dev
```

Then open browser console to see API logs.

## Files Created Summary

```
lib/
├── api-client.ts                    # Core API client (259 lines)
├── utils.ts                         # Existing utilities

hooks/
├── use-api.ts                       # API hook (97 lines)
└── use-api-error.ts                 # Error handling hook (121 lines)

components/
├── api-error-notification.tsx       # Error notification (86 lines)
└── api-example.tsx                  # Example component (194 lines)

Root:
├── .env.example                     # Environment template
├── .env.development.local           # Dev configuration (updated)
├── API_SETUP.md                     # Complete guide (383 lines)
├── API_QUICK_START.md               # Quick reference (253 lines)
└── FASTAPI_SETUP_COMPLETE.md        # This file
```

## Next Steps

1. **Configure Backend**: Set up FastAPI with CORS enabled
2. **Set Environment**: Copy `.env.example` to `.env.local`
3. **Update API URL**: Change `NEXT_PUBLIC_API_BASE_URL` to your backend URL
4. **Test Connection**: Use the example component to verify connectivity
5. **Integrate**: Start using API calls in your components
6. **Monitor**: Enable debug mode to troubleshoot issues

## Troubleshooting

### "Cannot find token"
- Check `setAuthToken()` is called after login
- Verify localStorage is enabled in browser

### "401 Unauthorized on valid token"
- Check token format (should be valid JWT)
- Verify backend is recognizing the Bearer prefix
- Check token hasn't expired

### "429 Too Many Requests"
- Implement retry delay in your code
- Check backend rate limit configuration
- Add exponential backoff retry logic

### "Network error"
- Verify backend is running on correct URL
- Check CORS configuration on backend
- Verify `NEXT_PUBLIC_API_BASE_URL` is correct

### "Timeout errors"
- Increase `NEXT_PUBLIC_API_TIMEOUT` if backend is slow
- Check network connectivity
- Verify backend is responding

## Support

For detailed information:
- See `API_SETUP.md` for comprehensive guide
- See `API_QUICK_START.md` for quick patterns
- Check `/components/api-example.tsx` for working examples
- Review error messages in browser console with debug mode enabled

---

**Setup Status**: ✅ Complete and Ready for Production

All files have been created and compiled successfully. The Next.js build completes without errors.
