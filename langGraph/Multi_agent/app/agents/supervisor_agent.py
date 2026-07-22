from app.agents.research_agent import ResearchAgent
from app.agents.writer_agent import WriterAgent
from app.agents.editor_agent import EditorAgent

class SupervisorAgent:
    def __init__(self):
        self.research = None
        self.writer = None
        self.editor = None
    
    async def initialize(self):
        self.research = await ResearchAgent().initialize()
        self.writer = await WriterAgent().initialize()
        self.editor = await EditorAgent().initialize()
        return self
    
    async def create_content(self, topic: str):
        print(f"📝 Generating content for: {topic}")
        
        # Step 1: Research
        print("🔍 Researching...")
        research_result = await self.research.run(topic)
        research_data = research_result["response"]
        
        # Step 2: Write
        print("✍️ Writing...")
        writer_result = await self.writer.run(research_data, topic)
        draft = writer_result["response"]
        
        # Step 3: Edit
        print("🔧 Editing...")
        editor_result = await self.editor.run(draft)
        final_content = editor_result["response"]
        
        print("✅ Content generated successfully!")
        
        return {
            "topic": topic,
            "research": research_data,
            "draft": draft,
            "final": final_content,
            "status": "complete"
        }