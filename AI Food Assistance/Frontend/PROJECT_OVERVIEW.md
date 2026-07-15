# BiteWise - Restaurant AI Food Assistant

## Project Overview

BiteWise is a comprehensive AI-powered restaurant assistant platform that includes customer-facing chat, admin dashboard, and detailed analytics. The system helps restaurants manage customer inquiries about menus, pricing, policies, and offers through an intelligent AI chatbot.

## Architecture

```
┌─────────────────┐
│   Public Pages  │
├─────────────────┤
│ / (Auth)        │ ← Login/Signup page
│ /home (Chat)    │ ← Customer chat interface
└─────────────────┘
         ↓ (JWT Token)
┌─────────────────┐
│  Protected Routes   │
├─────────────────┤
│ /admin          │ ← Admin dashboard
│ /analytics      │ ← Analytics dashboard
└─────────────────┘
         ↓ (JWT Verify)
┌─────────────────┐
│   API Routes    │
├─────────────────┤
│ /api/auth/*     │ ← Auth endpoints
│ /api/chat       │ ← Chat responses
└─────────────────┘
```

## Main Features

### 1. Authentication System
- **Location**: `/app/page.tsx`, `/api/auth/login`, `/api/auth/signup`
- **Technology**: JWT tokens, localStorage
- **Features**:
  - Username/password authentication
  - Email collection
  - Error handling for invalid credentials
  - 7-day token expiration
  - Persistent sessions

### 2. Customer Chat Interface
- **Location**: `/app/home/page.tsx`
- **Features**:
  - Real-time AI responses
  - Message history persistence
  - Thread management
  - Conversation threading
  - Category detection (Menu, Dietary, Policies, Offers)
  - Loading indicators during AI generation
  - Mobile responsive design

### 3. Admin Dashboard
- **Location**: `/app/admin/page.tsx`
- **Features**:
  - Stats cards (Documents, Queries, Threads, Users)
  - Recent questions table
  - Popular questions visualization
  - PDF upload interface with drag & drop
  - Document management
  - Export functionality
  - Tab-based navigation

### 4. Analytics Dashboard
- **Location**: `/app/analytics/page.tsx`
- **Features**:
  - Daily usage trend chart
  - Performance metrics
  - Popular questions analysis
  - Recent queries list
  - Date range filtering
  - JSON export with complete analytics data
  - Responsive layout for all devices

## Technology Stack

### Frontend
- **Framework**: Next.js 16 with React 19
- **Styling**: Tailwind CSS v4
- **UI Components**: Shadcn/ui
- **Charts**: Recharts
- **Icons**: Lucide React
- **Dates**: date-fns
- **Language**: TypeScript

### Backend
- **Runtime**: Next.js API Routes
- **Authentication**: JWT with jsonwebtoken
- **Storage**: localStorage (client-side session)
- **Data**: In-memory storage (demo)

### Development
- **Package Manager**: pnpm
- **Build Tool**: Turbopack (Next.js 16 default)
- **Linting**: ESLint

## File Structure

```
/vercel/share/v0-project/
├── app/
│   ├── page.tsx                 # Login/Signup
│   ├── home/
│   │   └── page.tsx            # Customer chat
│   ├── admin/
│   │   └── page.tsx            # Admin dashboard
│   ├── analytics/
│   │   └── page.tsx            # Analytics dashboard
│   ├── api/
│   │   ├── auth/
│   │   │   ├── login/route.ts
│   │   │   └── signup/route.ts
│   │   └── chat/route.ts
│   ├── layout.tsx              # Root layout
│   └── globals.css             # Global styles
├── components/
│   ├── login-form.tsx
│   ├── signup-form.tsx
│   ├── chat-window.tsx
│   ├── message-bubble.tsx
│   ├── chat-input.tsx
│   ├── chat-sidebar.tsx
│   ├── admin-sidebar.tsx
│   ├── stats-cards.tsx
│   ├── recent-questions-table.tsx
│   ├── popular-questions-chart.tsx
│   ├── pdf-upload-area.tsx
│   ├── analytics-header.tsx
│   ├── analytics-stats.tsx
│   ├── daily-usage-chart.tsx
│   ├── popular-questions-table.tsx
│   ├── recent-queries-list.tsx
│   └── date-range-filter.tsx
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.mjs
```

## Color Scheme

### Theme Colors
- **Primary**: Warm Orange (Food-associated) - #FF6B35 equivalent
- **Secondary**: Rich Brown - Spice tones
- **Accent**: Deep Orange - Complementary accent
- **Background**: Dark (#15, #20) - Professional dark theme
- **Foreground**: Light/White - High contrast text

### Design Tokens (OKLCH Color Space)
- Uses OKLCH color model for better perceptual uniformity
- Implements semantic tokens for consistency
- Dark mode as default with optional light mode support

## Key Metrics & Data

### Sample Analytics Data
- Total Queries: 342
- Documents Uploaded: 12
- Active Threads: 87
- Total Users: 45
- Daily Queries: 45-72 (7-day average)
- Top Question: "What's the biryani price?" (145 queries)

### Demo Credentials
- Username: `admin`
- Password: `password123`
- Email: `admin@bitwie.com`

### Restaurant Menu (Sample Data)
- Biryani: $12.99
- Kebab: $10.99
- Karahi: $11.99
- Nihari: $13.99
- Samosa: $3.99
- Lassi: $4.99

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login with username/password
- `POST /api/auth/signup` - New user registration

### Chat
- `POST /api/chat` - Get AI response for user query

## Security Features

- JWT token-based authentication
- HTTP-only localStorage for token storage
- Token expiration (7 days)
- Protected routes with auth checks
- Input validation
- Error handling for invalid credentials
- No sensitive data in client code

## Responsive Design

### Breakpoints
- **Mobile**: < 768px (iPhone, Android)
- **Tablet**: 768px - 1024px (iPad)
- **Desktop**: > 1024px (Desktop, Laptop)

### Adaptations
- Collapsible sidebars on mobile
- Stacked layouts for narrow screens
- Optimized touch targets
- Readable font sizes
- Proper spacing for mobile

## Performance Optimizations

- Code splitting with dynamic imports
- Image optimization with Next.js Image
- CSS optimization with Tailwind
- Bundle size minimization
- Client-side route transitions
- Efficient state management with React hooks

## Testing

### Tested Features
- ✅ Login/Signup authentication flow
- ✅ Chat message sending and receiving
- ✅ Thread history persistence
- ✅ Admin dashboard stats display
- ✅ PDF upload functionality
- ✅ Analytics data visualization
- ✅ Date range filtering
- ✅ JSON export functionality
- ✅ Mobile responsiveness
- ✅ Dark theme rendering

## Deployment

### Requirements
- Node.js 18+
- pnpm package manager

### Build & Run
```bash
# Install dependencies
pnpm install

# Development
pnpm dev

# Production build
pnpm build
pnpm start

# Linting
pnpm lint
```

### Environment Setup
- No external API keys required for demo
- In-memory data storage
- localStorage for session persistence

## Future Enhancements

### Phase 2 Features
- Real database integration (Neon/Supabase)
- Advanced user authentication (OAuth, passkeys)
- PDF parsing and document management
- Real-time chat with WebSockets
- Advanced analytics with ML insights
- Email notifications
- User profiles and preferences

### Phase 3 Features
- Multi-language support
- Voice chat interface
- Video tutorial integration
- CRM integration
- Reservation system
- Order tracking
- Payment integration
- Admin user management

## Documentation

- `AUTH_GUIDE.md` - Authentication implementation details
- `CHAT_FEATURES.md` - Chat interface features
- `ADMIN_DASHBOARD.md` - Admin dashboard documentation
- `ANALYTICS_DASHBOARD.md` - Analytics features and components
- `ANALYTICS_SUMMARY.md` - Quick reference for analytics

## Support & Troubleshooting

### Common Issues

**Chat not responding**
- Check API route is working: `POST /api/chat`
- Verify token is valid in localStorage
- Check browser console for errors

**Analytics not displaying**
- Ensure Recharts is installed: `pnpm add recharts`
- Verify date-fns is installed: `pnpm add date-fns`
- Check data format matches expected structure

**Mobile layout issues**
- Clear browser cache
- Check viewport meta tag in layout.tsx
- Verify Tailwind responsive classes

## License & Credits

Built with v0.app - Vercel's AI-powered code generation platform.

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Status**: Fully Functional Demo
