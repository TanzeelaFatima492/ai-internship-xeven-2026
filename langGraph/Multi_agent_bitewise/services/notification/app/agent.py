from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict, Literal, List, Dict, Any
import json
import uuid

# ==================== STATE ====================
class NotificationState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    notifications_sent: int
    last_action: str

# ==================== TOOLS ====================

@tool
def send_push_notification(user_id: str, title: str, message: str) -> str:
    """
    Send a push notification to a user.
    
    Args:
        user_id: The ID of the user to notify
        title: The title of the notification
        message: The message content
    
    Returns:
        Success or failure message
    """
    print(f"📱 [PUSH] To: {user_id} | {title}: {message}")
    return f"✅ Push notification sent to user {user_id}"


@tool
def send_email_notification(email: str, subject: str, body: str) -> str:
    """
    Send an email notification.
    
    Args:
        email: Recipient email address
        subject: Email subject
        body: Email body content
    
    Returns:
        Success or failure message
    """
    print(f"📧 [EMAIL] To: {email} | Subject: {subject}")
    return f"✅ Email sent to {email}"


@tool
def send_sms_notification(phone: str, message: str) -> str:
    """
    Send an SMS notification.
    
    Args:
        phone: Phone number to send SMS to
        message: SMS message content
    
    Returns:
        Success or failure message
    """
    print(f"📱 [SMS] To: {phone} | Message: {message[:50]}...")
    return f"✅ SMS sent to {phone}"


@tool
def get_user_notifications(user_id: str, limit: int = 10) -> str:
    """
    Get recent notifications for a user.
    
    Args:
        user_id: The ID of the user
        limit: Maximum number of notifications to return
    
    Returns:
        JSON string of notifications
    """
    # Mock data - replace with DB query
    notifications = [
        {"id": str(uuid.uuid4()), "message": "Your order is ready!", "read": False, "type": "order"},
        {"id": str(uuid.uuid4()), "message": "New offer available!", "read": False, "type": "offer"},
        {"id": str(uuid.uuid4()), "message": "Don't break your streak!", "read": True, "type": "streak"}
    ][:limit]
    
    return json.dumps({
        "user_id": user_id,
        "total": len(notifications),
        "notifications": notifications
    })


@tool
def mark_notification_read(user_id: str, notification_id: str) -> str:
    """
    Mark a notification as read.
    
    Args:
        user_id: The ID of the user
        notification_id: The ID of the notification
    
    Returns:
        Success or failure message
    """
    return f"✅ Notification {notification_id} marked as read for user {user_id}"


@tool
def send_bulk_notifications(user_ids: List[str], message: str) -> str:
    """
    Send a notification to multiple users.
    
    Args:
        user_ids: List of user IDs
        message: Message to send to all users
    
    Returns:
        Summary of sent notifications
    """
    count = len(user_ids)
    print(f"📢 [BULK] Sending to {count} users: {message}")
    return f"✅ Bulk notification sent to {count} users"


@tool
def format_notification(notification_type: str, data: Dict[str, str]) -> str:
    """
    Format a notification message based on type.
    
    Args:
        notification_type: Type (order_confirmation, offer, streak, routine, re_engagement)
        data: Dictionary with template variables
    
    Returns:
        Formatted message string
    """
    templates = {
        "order_confirmation": "✅ Order #{order_id} confirmed! Total: ${total}",
        "order_delivered": "🚚 Order #{order_id} delivered! Enjoy your meal!",
        "offer_available": "🎉 New offer: {offer_name} - {discount}",
        "streak_warning": "🔥 Don't break your {streak}-day streak!",
        "routine_reminder": "⏰ Time to order your usual meal at {usual_time}!",
        "re_engagement": "👋 We miss you! It's been {days} days!"
    }
    template = templates.get(notification_type, "{message}")
    try:
        return template.format(**data)
    except KeyError:
        return template


@tool
def get_notification_stats(user_id: str) -> str:
    """
    Get notification statistics for a user.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        JSON string with notification stats
    """
    # Mock data - replace with DB query
    stats = {
        "user_id": user_id,
        "total": 25,
        "read": 18,
        "unread": 7,
        "read_rate": 72.0,
        "by_type": {
            "order": 10,
            "offer": 8,
            "streak": 7
        }
    }
    return json.dumps(stats)


# ==================== ALL TOOLS ====================
NOTIFICATION_TOOLS = [
    send_push_notification,
    send_email_notification,
    send_sms_notification,
    get_user_notifications,
    mark_notification_read,
    send_bulk_notifications,
    format_notification,
    get_notification_stats
]

# ==================== AGENT ====================
class NotificationAgent:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.llm = ChatOllama(
            model=model,
            temperature=0.7,
            base_url="http://localhost:11434"
        ).bind_tools(NOTIFICATION_TOOLS)
        
        self.tool_node = ToolNode(NOTIFICATION_TOOLS)
        self.memory = MemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        
        def call_agent(state: NotificationState):
            response = self.llm.invoke(state["messages"])
            return {"messages": [response]}
        
        workflow = StateGraph(NotificationState)
        
        # Add nodes
        workflow.add_node("agent", call_agent)
        workflow.add_node("tools", self.tool_node)
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                END: END
            }
        )
        workflow.add_edge("tools", "agent")
        
        return workflow.compile(checkpointer=self.memory)
    
    async def run(self, user_id: str, query: str, thread_id: str = None) -> Dict:
        """Run the agent with a user query"""
        thread_id = thread_id or f"notification-{user_id}-{uuid.uuid4().hex[:8]}"
        
        config = {"configurable": {"thread_id": thread_id}}
        
        result = await self.graph.ainvoke(
            {
                "messages": [{"role": "user", "content": query}],
                "user_id": user_id,
                "notifications_sent": 0,
                "last_action": ""
            },
            config=config
        )
        
        # Extract final response
        messages = result.get("messages", [])
        final_response = messages[-1].content if messages else "No response"
        
        return {
            "user_id": user_id,
            "thread_id": thread_id,
            "response": final_response,
            "notifications_sent": result.get("notifications_sent", 0)
        }
    
    async def stream(self, user_id: str, query: str, thread_id: str = None):
        """Stream the agent's response"""
        thread_id = thread_id or f"notification-{user_id}-{uuid.uuid4().hex[:8]}"
        
        config = {"configurable": {"thread_id": thread_id}}
        
        async for event in self.graph.astream(
            {
                "messages": [{"role": "user", "content": query}],
                "user_id": user_id
            },
            config=config
        ):
            yield event


# ==================== SINGLETON INSTANCE ====================
notification_agent = None

def get_notification_agent():
    global notification_agent
    if notification_agent is None:
        notification_agent = NotificationAgent()
    return notification_agent