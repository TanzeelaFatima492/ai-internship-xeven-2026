# BiteWise Restaurant AI Chat Assistant

## Overview

BiteWise is a modern, intelligent chat interface for restaurant customers to inquire about menu items, pricing, special offers, policies, and more. Built with React, Next.js 16, and featuring a warm Pakistani restaurant aesthetic with dark theme.

## Features

### Chat Interface
- **Message Bubbles**: User messages appear on the right (orange/warm gradient), AI responses on the left (card-styled)
- **Auto-scrolling**: Messages automatically scroll into view as new ones arrive
- **Timestamps**: Each message shows when it was sent for conversation tracking
- **Loading State**: Animated spinner shows when AI is generating responses

### AI Response Metadata
- **Source Document**: Shows which menu section the item comes from (e.g., "Menu - Biryani")
- **Pricing**: Displays item prices directly in the response bubble
- **Rich Content**: Multi-line responses with formatted information about offers and policies

### Sidebar History
- **Thread History**: All previous conversations are saved and listed chronologically
- **Quick Access**: Click any thread to load full conversation history
- **Thread Preview**: Shows conversation title and creation timestamp
- **Active Highlight**: Currently active thread is highlighted with a colored border
- **New Chat Button**: Quick access button to start fresh conversations
- **Mobile Responsive**: Sidebar collapses on mobile, accessible via menu button

### Chat Input
- **Smart Input**: Textarea with proper handling of multiline text
- **Send Button**: Gradient button that disables when empty
- **Keyboard Shortcuts**: 
  - Enter key submits message
  - Shift+Enter creates new line
  - Handles CJK (Chinese/Japanese/Korean) IME composition correctly
- **Placeholder**: Helpful prompt text guides users on what they can ask

### Responsive Design
- **Desktop (1920x1080+)**: Full sidebar visible, optimal chat area width
- **Tablet (768px+)**: Sidebar visible with adjusted spacing
- **Mobile (375px-667px)**: 
  - Sidebar collapses by default
  - Menu button in header to toggle sidebar
  - Optimized touch targets
  - Single-column layout
  - Scaled message bubbles for readability

## User Interactions

### Asking About Menu Items
```
User: "What's your biryani price?"
AI Response: 
  "Chicken Biryani: Fragrant basmati rice with tender chicken, aromatic spices. 
   We carefully select premium ingredients and cook each dish to perfection. 
   Highly recommended!"
   
   Source: Menu - Biryani
   Price: $12.99
```

### Asking About Special Offers
```
User: "Tell me about offers"
AI Response: 
  "Great question! Here are our current offers:
   
   Family Combo: Biryani + 2 Kebabs + Samosa + Lassi = $39.99 (Save $5!)
   Lunch Special: Any main dish + rice + bread + drink = $9.99 (11 AM - 3 PM)
   20% off on orders above $25 using code BITEWISE20"
```

### Asking About Policies
```
User: "What are your delivery hours?"
AI Response:
  "Delivery: Free delivery on orders over $30. Delivery time: 30-45 minutes
   Hours: Open 11 AM - 11 PM, 7 days a week
   Reservations: Reservations available for groups of 4+. Call or book online"
```

## Technical Architecture

### Components

1. **HomePage** (`/app/home/page.tsx`)
   - Main chat interface container
   - Manages thread state and user authentication
   - Handles thread selection and creation

2. **ChatWindow** (`/components/chat-window.tsx`)
   - Core chat display area
   - Manages message list and input
   - Handles API calls to AI chat endpoint
   - Auto-scroll functionality

3. **ChatSidebar** (`/components/chat-sidebar.tsx`)
   - Thread history display
   - Mobile-responsive design
   - Thread navigation and new chat button

4. **MessageBubble** (`/components/message-bubble.tsx`)
   - Individual message rendering
   - Source and price metadata display
   - Styling differentiation for user vs. AI messages

5. **ChatInput** (`/components/chat-input.tsx`)
   - Input textarea with smart handling
   - Send button with state management
   - IME composition handling

### API Endpoint

**Route**: `/api/chat` (POST)

**Request Body**:
```json
{
  "message": "string - User's question",
  "history": "array - Previous messages in conversation",
  "userId": "string - Username of the user"
}
```

**Response**:
```json
{
  "message": "string - AI's response",
  "source": "string - Optional: Menu section or document source",
  "price": "string - Optional: Price information if menu item"
}
```

### Data Flow

1. User types message in input box
2. User clicks send or presses Enter
3. Message added to UI and sent to API
4. API processes message using intent detection
5. AI returns response with metadata
6. Response displayed with source and price (if applicable)
7. Conversation saved to localStorage
8. Thread added to history sidebar

### Storage

- **LocalStorage Keys**:
  - `token`: JWT authentication token
  - `chatThreads`: Array of all conversation threads with messages

- **Thread Structure**:
```javascript
{
  id: "thread-${timestamp}",
  title: "First 50 chars of initial message",
  createdAt: Date,
  preview: "Full preview text",
  messages: [/* array of Message objects */]
}
```

## AI Response Logic

The chat API uses pattern matching to detect user intent:

### Intent Detection
- **Menu Items**: Checks for dish names (biryani, kebab, karahi, nihari, samosa, lassi)
- **Pricing**: Keywords like "price", "how much", "cost"
- **Offers**: Keywords like "offer", "discount", "special", "deal"
- **Policies**: Keywords like "delivery", "hours", "open", "return", "refund", "reservation"
- **Browse Menu**: Keywords like "menu", "what", "recommend", "popular"

### Sample Menu Database
- Chicken Biryani - $12.99
- Seekh Kebab - $10.99
- Chicken Karahi - $11.99
- Beef Nihari - $13.99
- Vegetable Samosa - $3.99
- Mango Lassi - $4.99

### Special Offers
- Family Combo: $39.99 (Save $5)
- Lunch Special: $9.99 (11 AM - 3 PM)
- Delivery Discount: 20% off with code BITEWISE20

## Color Theme

### Dark Theme with Warm Food Colors
- **Background**: Deep dark navy/black (#15 0% 0%)
- **Primary**: Warm orange/spice color (#65 0.22 35)
- **Accent**: Brighter orange (#70 0.25 38)
- **Secondary**: Deep brown/rust (#55 0.18 30)
- **Card**: Slightly lighter dark background (#22 0.04 280)
- **Text**: Cream/off-white (#95 0.02 280)

### Styling
- User messages: Gradient from primary (orange) to accent (bright orange)
- AI messages: Card style with border
- Buttons: Gradient backgrounds with smooth transitions
- Sidebar: Slightly lighter background for contrast

## Mobile Optimizations

1. **Responsive Typography**: Smaller on mobile, larger on desktop
2. **Touch-Friendly**: Larger button/clickable areas (40px+ minimum)
3. **Simplified Layout**: Single column on mobile
4. **Collapsible Sidebar**: Hidden by default, toggled via menu
5. **Optimized Input**: Textarea scales appropriately
6. **Message Bubbles**: Max width constraints for readability

## Performance Considerations

- **Message Virtualization**: Displays all messages (can be optimized with virtualization for 1000+ messages)
- **LocalStorage Limits**: Browser localStorage has ~5-10MB limit per domain
- **API Response Time**: Simulated 500ms delay for realistic chat experience
- **Auto-scroll**: Smooth scrolling for better UX

## Future Enhancements

1. **Real AI Integration**: Connect to GPT/Claude API for intelligent responses
2. **Menu Management**: Admin panel to update menu items and prices
3. **Analytics**: Track popular questions and user behavior
4. **Push Notifications**: Notify users of new offers
5. **Favorites**: Save favorite menu items
6. **Image Support**: Add dish images to AI responses
7. **Multi-language**: Support for Urdu and other languages
8. **Message Search**: Search through conversation history
9. **Export Chat**: Download conversation as PDF
10. **Feedback System**: Rate helpful responses

## Testing

### Test Queries
1. "What's your biryani price?" → Menu item + price
2. "Tell me about offers" → All current offers
3. "What are your delivery hours?" → Delivery and hours info
4. "Do you have samosas?" → Menu browsing
5. "What's recommended?" → Popular dishes suggestion

### Responsive Testing
- Desktop: 1920x1080
- Tablet: 768x1024
- Mobile: 375x667 (iPhone 14)

## Deployment

1. Ensure environment variables are set for authentication
2. Deploy to Vercel using `vercel deploy`
3. Verify localStorage persistence in production
4. Test chat API endpoint after deployment
5. Monitor API response times and error rates

## Support

For issues or feature requests, contact the development team. Common troubleshooting:

- **Chat not loading**: Check browser console for errors
- **Messages not sending**: Verify API endpoint is accessible
- **History not saving**: Check localStorage is enabled
- **Mobile sidebar not working**: Clear browser cache and reload
