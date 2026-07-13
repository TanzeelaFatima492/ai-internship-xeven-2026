# Admin Dashboard Documentation

## Overview

The BiteWise Admin Dashboard provides comprehensive management and analytics tools for restaurant administrators. It includes real-time performance metrics, document management, conversation tracking, and data export capabilities.

## Access Requirements

- **Authentication**: JWT token required (login at `/` first)
- **URL**: `/admin`
- **Role**: Admin access (demo: `admin` / `password123`)

## Dashboard Features

### 1. Main Dashboard Tab

#### Stats Cards
The dashboard displays four key performance metrics:

- **Total Documents**: Number of uploaded PDF documents (12 in demo)
  - Trend indicator: "+2 this week"
  - Shows restaurant menu and policy documents

- **Total Queries**: Cumulative user questions/requests (342 in demo)
  - Trend indicator: "+48 today"
  - Tracks all customer interactions

- **Conversation Threads**: Active user conversations (87 in demo)
  - Trend indicator: "+12 this week"
  - Individual chat sessions

- **Active Users**: Current active users (45 in demo)
  - Trend indicator: "+8 new users"
  - Daily active users

Each stat card includes:
- Icon with gradient background
- Title and value
- Weekly/daily trend indicator
- Color-coded visualization

#### Recent Questions Table

Displays the latest user queries from the past 24 hours with:
- **Question**: The user's query text
- **User**: Customer name who asked
- **Category**: Question type (Menu, Dietary, Policies, Offers)
  - Menu: Orange badge
  - Dietary: Accent color badge
  - Policies: Secondary color badge
  - Offers: Green badge
- **Time**: Relative time (5 minutes ago, 1 hour ago, etc.)

Sample questions tracked:
- Menu pricing inquiries
- Dietary restrictions
- Delivery and policies
- Special offers

#### Popular Questions Chart

Bar chart showing the most frequently asked questions:
- "What are your prices?" - 84 queries (24%)
- "Do you deliver?" - 72 queries (21%)
- "Menu recommendations" - 56 queries (16%)
- "Dietary restrictions" - 45 queries (13%)
- "Current offers" - 38 queries (11%)
- "Reservation info" - 28 queries (8%)
- "Timing/Hours" - 19 queries (7%)

Includes:
- Question text
- Absolute count
- Percentage of total
- Visual progress bar
- "View Full Analytics" link

### 2. Upload PDF Tab

#### Drag & Drop Upload Area

Features:
- Large drop zone for PDF files
- Click to browse alternative
- Multiple file support
- 50MB file size limit per file
- Real-time progress tracking

#### File Upload Process

1. Drag PDF files into the upload area or click to browse
2. Selected files appear in the upload list
3. Upload progress shown with:
   - File name
   - File size
   - Progress bar with percentage
   - Status indicator

#### Upload Status Indicators

- **Uploading**: Blue progress bar with percentage
- **Success**: Green checkmark with "Upload completed successfully"
- **Error**: Red alert with retry option

#### Upload Information

Supported formats:
- PDF documents
- Menu files
- Policy documents

Best practices:
- Clear, readable PDF scans
- Organize by category
- Update regularly

### 3. Analytics Tab

Extended analytics dashboard for:
- Detailed performance metrics
- User behavior analysis
- Query trending
- Document performance

*Currently showing placeholder for future enhancement*

### 4. Threads Tab

Conversation thread management:
- View all user conversations
- Analyze specific threads
- Export conversation data
- User engagement metrics

*Currently showing placeholder for future enhancement*

### 5. Export Tab

Data export options with three main exports:

- **Query Report**
  - All user queries and AI responses
  - Question-answer pairs
  - Category tags
  - Timestamp data
  - Click download icon to export

- **User Analytics**
  - User engagement metrics
  - Activity timelines
  - Frequently queried users
  - Geographic data (if available)
  - Click download icon to export

- **Document List**
  - All uploaded documents
  - Upload dates
  - File sizes
  - Document metadata
  - Click download icon to export

Each export card includes:
- Icon
- Title
- Description
- Download button

## Sidebar Navigation

The left sidebar provides quick access to all dashboard sections:

- **Dashboard**: Main overview and stats
- **Upload PDF**: Document management interface
- **Analytics**: Detailed insights and metrics
- **Threads**: Conversation management
- **Export**: Data export tools

### Mobile Behavior

On mobile devices (< 1024px):
- Sidebar collapses by default
- Hamburger menu icon in header
- Sidebar slides in as overlay
- Click outside to close

### Desktop Behavior

On desktop (≥ 1024px):
- Sidebar always visible
- Fixed width (256px)
- Sticky positioning
- No collapse needed

## Responsive Design

### Mobile (< 768px)
- Single column layout
- Full-width cards
- Stacked navigation
- Touch-friendly buttons

### Tablet (768px - 1024px)
- Two column stats grid
- Responsive tables
- Optimized spacing

### Desktop (> 1024px)
- Multi-column layouts
- Side-by-side panels
- Sidebar navigation
- Full feature set

## Color Theme

The admin dashboard uses the warm Pakistani restaurant aesthetic:

- **Primary**: Orange (#E67E22) - Action buttons, active states
- **Accent**: Warm orange accent for highlights
- **Secondary**: Brown tones for secondary elements
- **Background**: Dark navy (#1a1a2e) - Professional dark theme
- **Cards**: Slightly lighter cards (#252a3e) for contrast
- **Text**: Light text on dark background for readability

## User Experience Features

### Loading States
- Spinning loader when dashboard initializes
- Progress indicators during data fetch
- Skeleton loaders for content sections

### Error Handling
- Toast notifications for errors
- Retry buttons for failed operations
- Clear error messages

### Accessibility
- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard navigation support
- High contrast text
- Focus indicators on interactive elements

## Security Features

### Authentication
- JWT token validation on page load
- Auto-redirect to login if token missing/invalid
- Logout clears token and redirects

### Data Protection
- Client-side token handling
- Secure API endpoints
- HTTPS recommended for production

## Performance Optimizations

- Lazy loading of components
- Optimized table rendering
- Efficient re-renders
- CSS-in-JS optimization
- Image/icon optimization

## Future Enhancements

Planned features:
- Real-time analytics with WebSocket updates
- Advanced filtering and search
- Date range selectors
- Custom report generation
- Email scheduling for exports
- Multi-language support
- Role-based access control
- Audit logging

## Troubleshooting

### Dashboard Not Loading
- Check JWT token in localStorage
- Clear cookies and refresh
- Verify admin credentials
- Check browser console for errors

### Upload Issues
- Verify PDF file format
- Check file size (< 50MB)
- Ensure stable internet connection
- Try different browser

### Missing Data
- Refresh the page
- Check data in customer chat interface
- Verify document uploads completed
- Check API connectivity

## Keyboard Shortcuts

- `Esc`: Close mobile sidebar
- `Tab`: Navigate between sections
- `Enter`: Activate buttons

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the dev console for errors
- Check API endpoint responses
- Contact support team
