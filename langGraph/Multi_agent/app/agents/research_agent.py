from app.agents.base_agent import BaseAgent
from app.tools.web_search import web_search_tool
from app.tools.news_tool import get_news_tool

class ResearchAgent:
    def __init__(self):
        self.agent = None
    
    async def initialize(self):
        tools = [web_search_tool, get_news_tool]
        system_prompt = """
        You are a Research Agent. Your job is to gather comprehensive information.
        
        Tools:
        1. web_search_tool: Search internet for information
        2. get_news_tool: Get latest news on topics
        
        Collect information from multiple sources.
        Format output as: [Source]: [Information]
        """
        self.agent = await BaseAgent(
            name="ResearchAgent",
            system_prompt=system_prompt,
            tools=tools
        ).initialize()
        return self
    
    async def run(self, topic: str):
        return await self.agent.run(f"Research: {topic}")