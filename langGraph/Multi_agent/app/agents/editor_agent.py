from app.agents.base_agent import BaseAgent
from app.tools.grammar_check import grammar_check

class EditorAgent:
    def __init__(self):
        self.agent = None
    
    async def initialize(self):
        tools = [grammar_check]
        system_prompt = """
        You are an Editor Agent. Your job is to improve content.
        
        Tools:
        1. grammar_check: Check grammar and spelling
        
        Fix grammar, improve readability, and suggest improvements.
        """
        self.agent = await BaseAgent(
            name="EditorAgent",
            system_prompt=system_prompt,
            tools=tools
        ).initialize()
        return self
    
    async def run(self, draft: str):
        return await self.agent.run(f"Edit and improve: {draft}")