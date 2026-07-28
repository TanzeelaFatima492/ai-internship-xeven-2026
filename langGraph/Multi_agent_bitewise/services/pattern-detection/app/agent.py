from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict, Dict
import json
import uuid
import requests

# ==================== STATE ====================
class PatternState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    last_action: str

# ==================== TOOLS ====================

@tool
def get_user_patterns(user_id: str) -> str:
    """Get complete user behavior patterns."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            return json.dumps({"success": True, "user_id": user_id, "patterns": response.json()})
        return json.dumps({"success": False, "error": "Pattern not found"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def detect_routine(user_id: str) -> str:
    """Detect user's ordering routine."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            data = response.json()
            routine = data.get("routine", {})
            return json.dumps({
                "success": True,
                "user_id": user_id,
                "routine": routine.get("routine", "unknown"),
                "usual_time": routine.get("usual_time"),
                "confidence": routine.get("confidence", 0)
            })
        return json.dumps({"success": False, "error": "Pattern not found"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def detect_preferences(user_id: str) -> str:
    """Detect user's food preferences."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            data = response.json()
            preferences = data.get("preferences", {})
            return json.dumps({
                "success": True,
                "user_id": user_id,
                "favorites": preferences.get("favorites", []),
                "categories": preferences.get("categories", []),
                "combos": preferences.get("combos", [])
            })
        return json.dumps({"success": False, "error": "Pattern not found"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def detect_spending(user_id: str) -> str:
    """Detect user's spending patterns."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            data = response.json()
            spending = data.get("spending", {})
            return json.dumps({
                "success": True,
                "user_id": user_id,
                "average": spending.get("average", 0),
                "trend": spending.get("trend", "stable"),
                "total_spent": spending.get("total_spent", 0)
            })
        return json.dumps({"success": False, "error": "Pattern not found"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def calculate_streak(user_id: str) -> str:
    """Calculate user's order streak."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            data = response.json()
            streak = data.get("streak", 0)
            return json.dumps({
                "success": True,
                "user_id": user_id,
                "streak": streak,
                "message": f"🔥 {streak} day streak!" if streak > 0 else "No streak yet"
            })
        return json.dumps({"success": False, "error": "Pattern not found"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def get_order_history(user_id: str, limit: int = 10) -> str:
    """Get user's order history."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/orders")
        if response.status_code == 200:
            data = response.json()
            orders = data.get("orders", [])[:limit]
            return json.dumps({
                "success": True,
                "user_id": user_id,
                "total_orders": data.get("total_orders", 0),
                "orders": orders
            })
        return json.dumps({"success": False, "error": "Orders not found"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def get_user_insights(user_id: str) -> str:
    """Get overall insights about user behavior."""
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            data = response.json()
            routine = data.get("routine", {})
            preferences = data.get("preferences", {})
            spending = data.get("spending", {})
            streak = data.get("streak", 0)
            insights = {
                "user_id": user_id,
                "total_orders": data.get("total_orders", 0),
                "routine_type": routine.get("routine", "unknown"),
                "favorite_items": [f.get("name") for f in preferences.get("favorites", [])[:3]],
                "average_spend": spending.get("average", 0),
                "streak": streak
            }
            return json.dumps({"success": True, "user_id": user_id, "insights": insights})
        return json.dumps({"success": False, "error": "Insights not available"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

# ==================== ALL TOOLS ====================
PATTERN_TOOLS = [
    get_user_patterns,
    detect_routine,
    detect_preferences,
    detect_spending,
    calculate_streak,
    get_order_history,
    get_user_insights
]

# ==================== AGENT ====================
class PatternAgent:
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
        self.llm = ChatOllama(
            model=model,
            temperature=0.3,
            base_url="http://localhost:11434"
        ).bind_tools(PATTERN_TOOLS)
        self.tool_node = ToolNode(PATTERN_TOOLS)
        self.memory = MemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        def call_agent(state: PatternState):
            response = self.llm.invoke(state["messages"])
            return {"messages": [response]}
        
        workflow = StateGraph(PatternState)
        workflow.add_node("agent", call_agent)
        workflow.add_node("tools", self.tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
        workflow.add_edge("tools", "agent")
        return workflow.compile(checkpointer=self.memory)
    
    async def run(self, user_id: str, query: str, thread_id: str = None) -> Dict:
        thread_id = thread_id or f"pattern-{user_id}-{uuid.uuid4().hex[:8]}"
        config = {"configurable": {"thread_id": thread_id}}
        result = await self.graph.ainvoke(
            {"messages": [{"role": "user", "content": query}], "user_id": user_id, "last_action": ""},
            config=config
        )
        messages = result.get("messages", [])
        final_response = messages[-1].content if messages else "No response"
        return {"user_id": user_id, "thread_id": thread_id, "response": final_response}

# ==================== SINGLETON ====================
pattern_agent = None

def get_pattern_agent():
    global pattern_agent
    if pattern_agent is None:
        pattern_agent = PatternAgent()
    return pattern_agent