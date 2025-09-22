# Chatbot Application

## Overview
Build a React-based chatbot interface that interacts with our backend API. When a user sends a message, the backend automatically generates and stores a bot response. This challenge assesses your ability to create a polished, functional chat interface with proper state management, error handling, and user experience considerations.

## Backend Setup
```bash
python3 main.py
```
The server will run on `http://localhost:8000`

## API Documentation

### 1. Send Message
**POST** `/api/message`

Request Body:
```json
{
  "message": "string"
}
```

Response (201 Created) with last 10 messages:
```json
{
  "user_message": {
    "id": 1,
    "username": "User",
    "message": "Hello bot",
    "timestamp": "2024-01-20T10:30:00.000Z"
  },
  "bot_response": {
    "id": 2,
    "username": "Bot",
    "message": "Hello! How can I assist you today?",
    "timestamp": "2024-01-20T10:30:01.000Z"
  }
}
```

Error Response (400):
```json
{
  "error": "Message cannot be empty"
}
```

### 2. Get Messages
**GET** `/api/messages?limit=50&offset=0`

Query Parameters:
- `limit` (optional): Number of messages to retrieve (default: 50)
- `offset` (optional): Number of messages to skip for pagination (default: 0)

Response (200 OK):
```json
{
  "messages": [
    {
      "id": 1,
      "username": "User",
      "message": "Hello",
      "timestamp": "2024-01-20T10:30:00.000Z"
    },
    {
      "id": 2,
      "username": "Bot",
      "message": "Hello! How can I assist you today?",
      "timestamp": "2024-01-20T10:30:01.000Z"
    }
  ]
}
```

## Requirements

### Core Functionality
1. **Message Display**: Show all messages in a chat bubble format (User on right, Bot on left)
2. **Send Messages**: Input field with send button to submit messages
3. **Auto-scroll**: Automatically scroll to latest message
4. **Loading States**: Show when waiting for bot response
5. **Error Handling**: Handle network errors and display user-friendly messages
6. **Message History**: Load and display conversation history on page load

### Technical Requirements
1. Use React (hooks preferred)
2. Implement proper state management (Context API, Redux, or Zustand)
3. Handle CORS (backend allows all origins)
4. Responsive design that works on mobile and desktop
5. Loading states for async operations
6. Input validation (no empty messages)

### Bonus Points
1. **Typing indicator**: Show "Bot is typing..." while waiting for response
2. **Message timestamps**: Format timestamps nicely (e.g., "2:30 PM" or "2 minutes ago")
3. **Smooth animations**: Message appearance, scroll behavior
4. **Keyboard shortcuts**: Enter to send, Shift+Enter for new line
5. **Empty state**: Nice UI when no messages exist
6. **Dark mode toggle**: Support light/dark themes
7. **Message persistence**: Save chat history in localStorage
8. **Accessibility**: ARIA labels, keyboard navigation, screen reader support
9. **Mobile responsive**: Works well on all screen sizes
10. **Unit tests**: Testing critical chat functionality

## Evaluation Criteria

### Code Quality (40%)
- Component structure and reusability
- State management approach
- Error boundary implementation
- Code organization and naming conventions
- TypeScript usage (if applicable)

### User Experience (30%)
- Smooth interactions and feedback
- Loading and error states
- Responsive design
- Keyboard shortcuts
- Performance optimization (memo, useCallback, etc.)

### Technical Implementation (30%)
- API integration patterns
- Error handling strategies
- Data flow architecture
- Browser compatibility
- Security considerations (XSS prevention)

## Time Expectation
2-3 hours for core functionality
+1 hour for bonus features

## Submission
1. Create a new React application
2. Implement the chat interface
3. Include a README with:
   - Setup instructions
   - Architecture decisions
   - Trade-offs made
   - Future improvements
   - Known limitations

## Notes for Interviewer
- Bot responses are automatically generated when user sends a message
- Database persists to `chat_messages.db` file
- CORS is enabled for all origins
- No WebSocket support (use polling for real-time feel)
- Bot has a 0.5 second delay to simulate thinking
- Simple pattern-based responses (greetings, questions, general)

## Common Pitfalls to Watch For
- Not differentiating User vs Bot messages visually
- Missing loading state while bot is "thinking"
- Not auto-scrolling to new messages
- Poor handling of rapid message sending
- Not clearing input after sending
- Memory leaks from polling intervals
- Direct DOM manipulation instead of React patterns
- Not handling Enter key for sending messages