# Analytics Dashboard Documentation

## Overview

The Analytics Dashboard provides comprehensive insights into restaurant AI assistant usage, user engagement, and system performance. It's accessible at `/analytics` and requires JWT authentication.

## Key Features

### 1. Stats Cards
Display four main metrics with trend indicators:
- **Total Queries**: 342 queries (12% trend)
- **Documents**: 12 documents uploaded (8% trend)
- **Active Threads**: 87 ongoing conversations (15% trend)
- **Total Users**: 45 active users (20% trend)

Each card features:
- Large, easy-to-read numbers
- Color-coded trend indicators (green for positive)
- Gradient background icons matching warm food theme
- Percentage change display

### 2. Daily Usage Trend Chart
Line chart visualization using Recharts showing:
- Queries per day over the past 7 days
- X-axis: Date labels (Dec 1 - Dec 7)
- Y-axis: Query count
- Gradient line with dot indicators
- Responsive sizing (full width on mobile, 2/3 on desktop)

**Data Points:**
- Dec 1: 45 queries
- Dec 2: 52 queries
- Dec 3: 48 queries
- Dec 4: 61 queries
- Dec 5: 55 queries
- Dec 6: 67 queries
- Dec 7: 72 queries

### 3. Popular Questions Section
Sidebar table (1/3 width on desktop) showing:
- Top 5 asked questions with count and percentage
- Visual progress bars showing relative popularity
- Color-coded count badges

**Top Questions:**
1. "What's the biryani price?" - 145 queries (42.4%)
2. "Do you have vegetarian options?" - 98 queries (28.7%)
3. "What are delivery hours?" - 67 queries (19.6%)
4. "Tell me about offers" - 45 queries (13.2%)
5. "How to place an order?" - 32 queries (9.4%)

### 4. Recent Queries List
Full-width section below charts showing:
- Latest 5 user queries with timestamps
- Category badges (Menu, Dietary, Policies, Offers)
- Relative time display (e.g., "5 minutes ago")
- Color-coded category indicators
- "View All Queries" button for pagination

### 5. Date Range Filter
Dropdown selector with preset options:
- Last 7 Days
- Last 30 Days
- Last 90 Days
- This Year

Current selection displayed as "Jun 12 - Jul 12"

### 6. Export Button
Orange gradient button to download analytics as JSON:
- Includes: Date range, stats, daily usage data, popular questions, recent queries
- File naming: `analytics-YYYY-MM-DD.json`
- Supports downloading for external analysis

## Design

### Color Scheme
- **Background**: Dark theme (#15, #20, #2a theme)
- **Cards**: Slightly lighter than background (#22 theme)
- **Primary**: Warm orange (food-associated)
- **Accent**: Deep orange/brown
- **Secondary**: Rich brown tones
- **Text**: Light gray/white for contrast

### Layout
- **Desktop**: 
  - 4-column stats grid
  - 2-column layout: Chart (2/3) + Popular Questions (1/3)
  - Full-width recent queries list
  
- **Mobile**: 
  - 1-column stats (stacked)
  - Full-width chart and popular questions (stacked)
  - Full-width recent queries

### Typography
- Headers: Bold, larger font sizes
- Stats: Extra-large numbers for visual impact
- Labels: Medium weight, muted foreground color
- Descriptions: Small, light gray text

## Components

### `AnalyticsPage` (`app/analytics/page.tsx`)
Main page component handling:
- Authentication check with JWT
- Date range state management
- Export data generation
- Layout orchestration

### `AnalyticsHeader` (`components/analytics-header.tsx`)
Introductory section with:
- Trending icon
- Title and description
- Gradient background styling

### `AnalyticsStats` (`components/analytics-stats.tsx`)
4-column stat cards displaying:
- Key metrics with icons
- Trend percentages
- Gradient styling

### `DailyUsageChart` (`components/daily-usage-chart.tsx`)
Recharts line chart component:
- Sample data for 7-day period
- Responsive container
- Gradient line styling
- Interactive tooltips

### `PopularQuestionsTable` (`components/popular-questions-table.tsx`)
Sidebar component showing:
- Question text
- Query count with trending icon
- Percentage bar visualization
- Category distribution

### `RecentQueriesList` (`components/recent-queries-list.tsx`)
List component displaying:
- Recent queries with timestamps
- Category color badges
- Relative time formatting using `date-fns`
- Hover effects for interactivity

### `DateRangeFilter` (`components/date-range-filter.tsx`)
Date selector dropdown with:
- 4 preset time ranges
- Current date range display
- Calendar icon
- Dropdown menu with smooth transitions

## Authentication

All routes require valid JWT token stored in localStorage:
```javascript
const token = localStorage.getItem('token')
```

If token is missing or invalid, user is redirected to login page.

## Data Format

### Export JSON Structure
```json
{
  "exportDate": "2024-12-07T...",
  "dateRange": {
    "startDate": "2024-11-07T...",
    "endDate": "2024-12-07T..."
  },
  "stats": {
    "totalQueries": 342,
    "totalDocuments": 12,
    "activeThreads": 87,
    "totalUsers": 45
  },
  "dailyUsage": [
    { "date": "2024-12-01", "queries": 45 },
    ...
  ],
  "popularQuestions": [
    { "question": "...", "count": 145, "percentage": 42.4 },
    ...
  ],
  "recentQueries": [
    { "id": "1", "question": "...", "timestamp": "...", "category": "Menu" },
    ...
  ]
}
```

## Responsive Behavior

| Device | Changes |
|--------|---------|
| Mobile (< 768px) | Single column stats, full-width chart/questions, stacked layout |
| Tablet (768px - 1024px) | 2-column stats, side-by-side chart and questions |
| Desktop (> 1024px) | 4-column stats, 2/3 chart + 1/3 sidebar layout |

## Dependencies

- **recharts**: Line chart visualization
- **date-fns**: Date formatting and calculations
- **lucide-react**: Icons (TrendingUp, Calendar, etc.)
- **next/navigation**: URL routing and authentication checks

## Future Enhancements

- Custom date range picker (not just presets)
- More detailed analytics with breakdowns by category
- User behavior tracking and heatmaps
- Export to CSV and PDF formats
- Real-time updates with WebSocket
- Machine learning insights and predictions
- A/B testing analytics
- Integration with admin dashboard navigation

## Usage Example

```typescript
// Accessing the analytics page
router.push('/analytics')

// Exporting data programmatically
const analyticsData = {
  exportDate: new Date().toISOString(),
  dateRange: { startDate, endDate },
  stats: { totalQueries, totalDocuments, ... },
  // ... rest of data
}

const dataStr = JSON.stringify(analyticsData, null, 2)
const dataBlob = new Blob([dataStr], { type: 'application/json' })
// ... download blob
```

## Troubleshooting

### Charts not rendering
- Ensure Recharts is installed: `pnpm add recharts`
- Check browser console for errors
- Verify data format matches expected structure

### Dates not formatting correctly
- Ensure date-fns is installed: `pnpm add date-fns`
- Verify Date objects are valid instances

### Export button not working
- Check localStorage permissions
- Verify token exists in localStorage
- Ensure browser supports Blob API

---

Last Updated: December 2024
