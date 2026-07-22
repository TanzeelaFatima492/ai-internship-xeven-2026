from app.agents.base_agent import BaseAgent
from app.tools.document_writer import write_document

class WriterAgent:
    def __init__(self):
        self.agent = None
    
    async def initialize(self):
        tools = [write_document]
        system_prompt = """
        You are a Writer Agent. Your job is to create engaging content.
        
        Tools:
        1. write_document: Save content to file
        
        Write in a clear, professional style.
        Include headings, subheadings, and bullet points.
        """
        self.agent = await BaseAgent(
            name="WriterAgent",
            system_prompt=system_prompt,
            tools=tools
        ).initialize()
        return self
    
    async def run(self, research_data: str, topic: str):
        return await self.agent.run(f"""
        Write a blog post about: {topic}
        
        Research Data:
        {research_data}
        
        Create a well-structured article with:
        - Catchy title
        - Introduction
        - Main points (3-5)
        - Conclusion
        """)