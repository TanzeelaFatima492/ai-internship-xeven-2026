from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict, List, Dict, Any
import json
import uuid
import requests

# ==================== STATE ====================
class OfferState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    offers_generated: int
    last_action: str

# ==================== TOOLS ====================

@tool
def generate_routine_reminder(user_id: str, usual_time: str = None) -> str:
    """
    Generate a routine reminder offer based on user's ordering habit.
    
    Args:
        user_id: The ID of the user
        usual_time: Optional - time of day user usually orders
    
    Returns:
        Offer details as JSON string
    """
    # Call Pattern Detection service
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            profile = response.json()
            routine = profile.get("routine", {})
            if routine.get("routine") in ["consistent", "semi_consistent"]:
                usual_time = routine.get("usual_time", "14:00")
                offer = {
                    "type": "routine_reminder",
                    "message": f"⏰ Ready to order your usual meal at {usual_time}?",
                    "priority": "high",
                    "discount": "Free delivery"
                }
                return json.dumps(offer)
    except:
        pass
    
    # Fallback
    offer = {
        "type": "routine_reminder",
        "message": "⏰ Time to order your favorite meal!",
        "priority": "medium",
        "discount": "Free delivery"
    }
    return json.dumps(offer)


@tool
def generate_streak_protection(user_id: str) -> str:
    """
    Generate a streak protection offer based on user's order streak.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        Offer details as JSON string
    """
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            profile = response.json()
            streak = profile.get("streak", 0)
            if streak >= 3:
                offer = {
                    "type": "streak_protection",
                    "message": f"🔥 Don't break your {streak}-day streak! Order now!",
                    "priority": "high",
                    "discount": "15% off your order"
                }
                return json.dumps(offer)
    except:
        pass
    
    offer = {
        "type": "streak_protection",
        "message": "🔥 Keep your streak alive! Order now!",
        "priority": "medium",
        "discount": "10% off"
    }
    return json.dumps(offer)


@tool
def generate_re_engagement(user_id: str) -> str:
    """
    Generate a re-engagement offer for inactive users.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        Offer details as JSON string
    """
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            profile = response.json()
            last_order = profile.get("last_order")
            if last_order:
                from datetime import datetime
                last_date = datetime.fromisoformat(last_order)
                days_since = (datetime.now() - last_date).days
                if days_since >= 7:
                    offer = {
                        "type": "re_engagement",
                        "message": f"👋 We miss you! It's been {days_since} days!",
                        "priority": "high",
                        "discount": "25% off your next order"
                    }
                    return json.dumps(offer)
    except:
        pass
    
    offer = {
        "type": "re_engagement",
        "message": "👋 Come back! We have a special offer for you!",
        "priority": "medium",
        "discount": "20% off"
    }
    return json.dumps(offer)


@tool
def generate_combo_deal(user_id: str) -> str:
    """
    Generate a combo deal based on frequently paired items.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        Offer details as JSON string
    """
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            profile = response.json()
            combos = profile.get("preferences", {}).get("combos", [])
            if combos:
                top_combo = combos[0]
                items = top_combo.get("items", [])
                if items and len(items) >= 2:
                    offer = {
                        "type": "combo_deal",
                        "message": f"🍔 Combo: {items[0]} + {items[1]} - Save 15%!",
                        "priority": "medium",
                        "discount": "15% off combo"
                    }
                    return json.dumps(offer)
    except:
        pass
    
    offer = {
        "type": "combo_deal",
        "message": "🍔 Combo deal available!",
        "priority": "low",
        "discount": "10% off combo"
    }
    return json.dumps(offer)


@tool
def generate_milestone_reward(user_id: str) -> str:
    """
    Generate a milestone reward based on total orders.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        Offer details as JSON string
    """
    try:
        response = requests.get(f"http://localhost:8001/user/{user_id}/patterns")
        if response.status_code == 200:
            profile = response.json()
            total_orders = profile.get("total_orders", 0)
            
            milestones = [5, 10, 25, 50, 100]
            for milestone in milestones:
                if total_orders == milestone:
                    offer = {
                        "type": "milestone_reward",
                        "message": f"🎉 {milestone} orders! You've earned a reward!",
                        "priority": "high",
                        "discount": "Free dessert"
                    }
                    return json.dumps(offer)
                elif total_orders > 0 and total_orders % 5 == 0:
                    offer = {
                        "type": "milestone_reward",
                        "message": f"🎉 {total_orders} orders and counting!",
                        "priority": "medium",
                        "discount": "10% off"
                    }
                    return json.dumps(offer)
    except:
        pass
    
    offer = {
        "type": "milestone_reward",
        "message": "🎉 You're on a roll! Keep ordering!",
        "priority": "low",
        "discount": "5% off"
    }
    return json.dumps(offer)


@tool
def generate_all_offers(user_id: str) -> str:
    """
    Generate all personalized offers for a user.
    
    Args:
        user_id: The ID of the user
    
    Returns:
        List of all offers as JSON string
    """
    offers = []
    
    # Call each offer generator
    offer_functions = [
        generate_routine_reminder,
        generate_streak_protection,
        generate_re_engagement,
        generate_combo_deal,
        generate_milestone_reward
    ]
    
    for func in offer_functions:
        try:
            result = func(user_id)
            offer = json.loads(result)
            offers.append(offer)
        except:
            pass
    
    # Send notifications for high priority offers
    try:
        for offer in offers:
            if offer.get("priority") == "high":
                requests.post(
                    "http://localhost:8003/notify",
                    json={
                        "user_id": user_id,
                        "message": offer.get("message"),
                        "type": offer.get("type"),
                        "data": {"offer": offer}
                    }
                )
    except:
        pass
    
    return json.dumps({
        "user_id": user_id,
        "total_offers": len(offers),
        "offers": offers
    })


@tool
def apply_offer(user_id: str, offer_type: str) -> str:
    """
    Apply an offer to the user's cart.
    
    Args:
        user_id: The ID of the user
        offer_type: Type of offer to apply
    
    Returns:
        Confirmation message
    """
    return json.dumps({
        "success": True,
        "message": f"✅ Offer '{offer_type}' applied to cart!",
        "discount_applied": True
    })


@tool
def get_offer_details(offer_type: str) -> str:
    """
    Get details about a specific offer type.
    
    Args:
        offer_type: Type of offer
    
    Returns:
        Offer details as JSON string
    """
    offer_details = {
        "routine_reminder": {
            "description": "Reminder to order at your usual time",
            "discount": "Free delivery",
            "validity": "Today only"
        },
        "streak_protection": {
            "description": "Keep your order streak alive",
            "discount": "15% off",
            "validity": "24 hours"
        },
        "re_engagement": {
            "description": "Welcome back offer for inactive users",
            "discount": "25% off",
            "validity": "7 days"
        },
        "combo_deal": {
            "description": "Discount on frequently paired items",
            "discount": "15% off combo",
            "validity": "3 days"
        },
        "milestone_reward": {
            "description": "Reward for reaching order milestones",
            "discount": "Free dessert or 10% off",
            "validity": "5 days"
        }
    }
    
    details = offer_details.get(offer_type, {
        "description": "Special offer",
        "discount": "Varies",
        "validity": "Check details"
    })
    
    return json.dumps({
        "type": offer_type,
        **details
    })

# ==================== ALL TOOLS ====================
OFFER_TOOLS = [
    generate_routine_reminder,
    generate_streak_protection,
    generate_re_engagement,
    generate_combo_deal,
    generate_milestone_reward,
    generate_all_offers,
    apply_offer,
    get_offer_details
]

# ==================== AGENT ====================
class OfferAgent:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.llm = ChatOllama(
            model=model,
            temperature=0.7,
            base_url="http://localhost:11434"
        ).bind_tools(OFFER_TOOLS)
        
        self.tool_node = ToolNode(OFFER_TOOLS)
        self.memory = MemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        
        def call_agent(state: OfferState):
            response = self.llm.invoke(state["messages"])
            return {"messages": [response]}
        
        workflow = StateGraph(OfferState)
        
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
        thread_id = thread_id or f"offer-{user_id}-{uuid.uuid4().hex[:8]}"
        
        config = {"configurable": {"thread_id": thread_id}}
        
        result = await self.graph.ainvoke(
            {
                "messages": [{"role": "user", "content": query}],
                "user_id": user_id,
                "offers_generated": 0,
                "last_action": ""
            },
            config=config
        )
        
        messages = result.get("messages", [])
        final_response = messages[-1].content if messages else "No response"
        
        return {
            "user_id": user_id,
            "thread_id": thread_id,
            "response": final_response,
            "offers_generated": result.get("offers_generated", 0)
        }
    
    async def stream(self, user_id: str, query: str, thread_id: str = None):
        """Stream the agent's response"""
        thread_id = thread_id or f"offer-{user_id}-{uuid.uuid4().hex[:8]}"
        
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
offer_agent = None

def get_offer_agent():
    global offer_agent
    if offer_agent is None:
        offer_agent = OfferAgent()
    return offer_agent