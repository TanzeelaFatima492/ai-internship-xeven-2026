from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict, Dict, List
import json
import uuid
import requests

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    current_step: str
    data: Dict

# ==================== TOOLS ====================

@tool
def analyze_user(user_id: str) -> str:
    """Call PatternAgent to analyze user behavior."""
    try:
        response = requests.post(
            "http://localhost:8001/agent/pattern",
            json={"user_id": user_id, "query": "Get my complete behavior patterns"}
        )
        if response.status_code == 200:
            data = response.json()
            return json.dumps({
                "success": True,
                "step": "analysis",
                "data": data.get("data", {})
            })
        return json.dumps({"success": False, "error": "Pattern analysis failed"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def generate_offers(user_id: str) -> str:
    """Call OfferAgent to generate personalized offers."""
    try:
        response = requests.post(
            "http://localhost:8002/agent/offers",
            json={"user_id": user_id, "query": "Generate all offers for me"}
        )
        if response.status_code == 200:
            data = response.json()
            return json.dumps({
                "success": True,
                "step": "offers",
                "data": data.get("data", {})
            })
        return json.dumps({"success": False, "error": "Offer generation failed"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def send_notification(user_id: str, message: str) -> str:
    """Call NotificationAgent to send alert."""
    try:
        response = requests.post(
            "http://localhost:8003/agent/notify",
            json={"user_id": user_id, "query": f"Send notification: {message}"}
        )
        if response.status_code == 200:
            data = response.json()
            return json.dumps({
                "success": True,
                "step": "notification",
                "data": data.get("data", {})
            })
        return json.dumps({"success": False, "error": "Notification failed"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@tool
def full_workflow(user_id: str) -> str:
    """Run complete workflow: Analyze → Offers → Notify."""
    try:
        analyze_result = json.loads(analyze_user(user_id))
        if not analyze_result.get("success"):
            return json.dumps({"success": False, "error": "Analysis failed"})
        
        offers_result = json.loads(generate_offers(user_id))
        if not offers_result.get("success"):
            return json.dumps({"success": False, "error": "Offer generation failed"})
        
        notify_result = json.loads(send_notification(
            user_id,
            "🎉 New personalized offers are ready for you!"
        ))
        
        return json.dumps({
            "success": True,
            "workflow": "complete",
            "analysis": analyze_result.get("data"),
            "offers": offers_result.get("data"),
            "notification": notify_result.get("data")
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

SUPERVISOR_TOOLS = [
    analyze_user,
    generate_offers,
    send_notification,
    full_workflow
]


class SupervisorAgent:
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
        self.llm = ChatOllama(
            model=model,
            temperature=0.3,
            base_url="http://localhost:11434"
        ).bind_tools(SUPERVISOR_TOOLS)
        self.tool_node = ToolNode(SUPERVISOR_TOOLS)
        self.memory = MemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        def call_agent(state: SupervisorState):
            response = self.llm.invoke(state["messages"])
            return {"messages": [response]}
        
        workflow = StateGraph(SupervisorState)
        workflow.add_node("agent", call_agent)
        workflow.add_node("tools", self.tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
        workflow.add_edge("tools", "agent")
        return workflow.compile(checkpointer=self.memory)
    
    async def run(self, user_id: str, query: str, thread_id: str = None) -> Dict:
        thread_id = thread_id or f"super-{user_id}-{uuid.uuid4().hex[:8]}"
        config = {"configurable": {"thread_id": thread_id}}
        result = await self.graph.ainvoke(
            {
                "messages": [{"role": "user", "content": query}],
                "user_id": user_id,
                "current_step": "",
                "data": {}
            },
            config=config
        )
        messages = result.get("messages", [])
        final_response = messages[-1].content if messages else "No response"
        return {"user_id": user_id, "thread_id": thread_id, "response": final_response}


supervisor = None

def get_supervisor():
    global supervisor
    if supervisor is None:
        supervisor = SupervisorAgent()
    return supervisor