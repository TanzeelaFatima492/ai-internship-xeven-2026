from langchain.agents import create_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_ollama import ChatOllama
import uuid

class BaseAgent:
    def __init__(self, name: str, system_prompt: str, tools: list):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools
        self.model = ChatOllama(
            model="llama3.2:latest",
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        self.agent = None
        self.checkpointer = None
    
    async def initialize(self):
        self.checkpointer = await AsyncSqliteSaver.from_conn_string("checkpoints.db")
        await self.checkpointer.setup()
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            checkpointer=self.checkpointer,
            system_prompt=self.system_prompt
        )
        return self
    
    async def run(self, query: str, thread_id: str = None):
        if thread_id is None:
            thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]},
            config
        )
        messages = response.get("messages", [])
        return {
            "success": True,
            "response": messages[-1].content if messages else "No response",
            "agent": self.name
        }