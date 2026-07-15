# FastAPI Integration - Implementation Checklist

## Setup Phase

- [ ] Read `API_QUICK_START.md` for overview
- [ ] Review `API_SETUP.md` for detailed information
- [ ] Check environment variables in `.env.example`
- [ ] Copy `.env.example` to `.env.local`
- [ ] Update `NEXT_PUBLIC_API_BASE_URL` with your FastAPI server URL

## Backend Preparation

- [ ] FastAPI server running on configured URL (default: `http://localhost:8000`)
- [ ] CORS middleware enabled for frontend URL
- [ ] JWT authentication endpoints implemented:
  - [ ] `POST /api/auth/login` - Returns JWT token
  - [ ] `POST /api/auth/signup` - Returns JWT token
- [ ] API endpoints return proper status codes:
  - [ ] 200 for success
  - [ ] 400 for bad request
  - [ ] 401 for unauthorized
  - [ ] 404 for not found
  - [ ] 429 for rate limiting
  - [ ] 500 for server errors

## Frontend Integration

### Token Management
- [ ] After login, call `setAuthToken(token)` to store JWT
- [ ] JWT automatically attached to all requests
- [ ] On logout, call `clearAuthToken()` to remove token
- [ ] Test with `getAuthToken()` to verify token storage

### Error Handling
- [ ] 401 errors automatically redirect to login
- [ ] 429 errors show rate limit warning
- [ ] Network errors show connection message
- [ ] Test error handling with invalid credentials
- [ ] Test rate limiting with rapid requests

### API Calls
- [ ] Replace hardcoded test data with real API calls
- [ ] Use `useApi` hook for loading states
- [ ] Use `useApiError` hook for error display
- [ ] Add `ApiErrorNotification` to error display
- [ ] Test all HTTP methods (GET, POST, PUT, PATCH, DELETE)

### Components to Update

For each API-dependent component:
- [ ] Import `useApi` or direct API functions
- [ ] Handle loading states
- [ ] Handle error states
- [ ] Display user feedback
- [ ] Test with real backend

Example components:
- [ ] Login form - POST to `/api/auth/login`
- [ ] Signup form - POST to `/api/auth/signup`
- [ ] Chat interface - POST to `/api/chat`
- [ ] Admin dashboard - GET analytics data
- [ ] Document upload - POST `/api/documents/upload`
- [ ] Analytics page - GET analytics endpoints

## Testing Checklist

### Basic Connectivity
- [ ] Start dev server: `pnpm dev`
- [ ] Navigate to app in browser
- [ ] Check console for errors
- [ ] Verify network tab shows API calls

### Authentication
- [ ] Login works and stores token
- [ ] Token appears in localStorage
- [ ] Token sent in Authorization header
- [ ] Token cleared on logout
- [ ] Expired token redirects to login

### Error Handling
- [ ] Invalid credentials show error
- [ ] Network down shows error message
- [ ] Timeout shows error message
- [ ] Rate limit shows warning
- [ ] Errors auto-dismiss or have close button

### API Operations
- [ ] GET requests fetch data correctly
- [ ] POST requests send data correctly
- [ ] PUT/PATCH requests update data
- [ ] DELETE requests remove data
- [ ] Response data properly typed

### Performance
- [ ] No console errors in dev tools
- [ ] Network requests complete in reasonable time
- [ ] Loading spinners show/hide appropriately
- [ ] No memory leaks with multiple requests
- [ ] Browser dev tools show proper performance

### Responsiveness
- [ ] Works on desktop (1920x1080)
- [ ] Works on tablet (768x1024)
- [ ] Works on mobile (375x667)
- [ ] Error messages display properly on all sizes
- [ ] Loading states visible on all sizes

## Configuration Verification

### Environment Variables
```bash
# Check that these are set:
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_STORAGE_KEY=bitewise_auth_token
NEXT_PUBLIC_API_TIMEOUT=30000
NEXT_PUBLIC_API_DEBUG=false  # Set to true for testing
```

### TypeScript
- [ ] No TypeScript errors: `pnpm tsc --noEmit`
- [ ] All API responses properly typed
- [ ] No `any` types in API files (except where necessary)

### Build
- [ ] Production build succeeds: `pnpm build`
- [ ] No warnings in build output
- [ ] Built files can start: `pnpm start`

## Security Checklist

- [ ] JWT token never exposed in logs (except debug mode)
- [ ] Token cleared on session expiration (401)
- [ ] No sensitive data in localStorage except token
- [ ] CORS properly configured on backend
- [ ] API calls use HTTPS in production
- [ ] Environment variables not exposed in browser except `NEXT_PUBLIC_*`

## Documentation & Maintenance

- [ ] README updated with API setup instructions
- [ ] Team members know how to:
  - [ ] Add new API endpoints
  - [ ] Handle specific error codes
  - [ ] Add request headers if needed
  - [ ] Test with different backends
- [ ] Error messages are user-friendly
- [ ] API debug mode can be enabled for troubleshooting
- [ ] Example component shows all patterns

## Deployment Checklist

### Staging
- [ ] Backend URL configured for staging
- [ ] Environment variables set in Vercel
- [ ] API calls work against staging backend
- [ ] Error handling works end-to-end
- [ ] Performance acceptable

### Production
- [ ] Backend URL configured for production
- [ ] Environment variables set in Vercel
- [ ] SSL/HTTPS enabled
- [ ] CORS configured for production domain
- [ ] API debug mode disabled
- [ ] Rate limiting tested
- [ ] Monitoring configured for API errors

## Quick Test Commands

```bash
# Start development server
pnpm dev

# Run type checking
pnpm tsc --noEmit

# Build for production
pnpm build

# Start production server
pnpm start

# Enable debug logging and start
NEXT_PUBLIC_API_DEBUG=true pnpm dev
```

## File Structure Verification

Verify all files exist:
```
✓ /lib/api-client.ts
✓ /hooks/use-api.ts
✓ /hooks/use-api-error.ts
✓ /components/api-error-notification.tsx
✓ /components/api-example.tsx
✓ /.env.example
✓ /.env.development.local
✓ /API_SETUP.md
✓ /API_QUICK_START.md
✓ /FASTAPI_SETUP_COMPLETE.md
✓ /IMPLEMENTATION_CHECKLIST.md
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 401 on valid token | Check backend JWT validation, verify token format |
| Token not persisting | Enable localStorage, check browser settings |
| CORS errors | Enable CORS middleware on FastAPI backend |
| Network errors | Verify backend URL is correct, backend is running |
| 429 rate limit errors | Add delay between requests, implement backoff |
| Timeout errors | Increase timeout value, check backend performance |

## Support Resources

- **API Setup Guide**: `/API_SETUP.md`
- **Quick Reference**: `/API_QUICK_START.md`
- **Complete Overview**: `/FASTAPI_SETUP_COMPLETE.md`
- **Working Examples**: `/components/api-example.tsx`
- **Error Handling**: `/hooks/use-api-error.ts`
- **API Client**: `/lib/api-client.ts`

---

## Sign Off

Once you've completed all items in this checklist:

- [ ] Date completed: _______________
- [ ] Developer name: _______________
- [ ] Tested by: _______________
- [ ] Ready for production: YES / NO

**Notes:**
_________________________________________________________________________________
_________________________________________________________________________________
