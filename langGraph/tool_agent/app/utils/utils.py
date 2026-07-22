import uuid
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.utils.agent_tools import ToolsHandler, system_prompt
from app.core.config import settings
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

async def handle_query(chatbot_schema):
    try:
        bot_id = chatbot_schema.bot_id
        query = chatbot_schema.query
        index_name = chatbot_schema.index_name
        
        if bot_id is None or bot_id == "":
            bot_id = str(uuid.uuid4())
            
        toolhandler = ToolsHandler(index_name)
        tools = [toolhandler.get_info_from_pinecone, toolhandler.web_search_tool]
        
        # 👇 Ollama model (choose any)
        llm = ChatOllama(
            model="llama3.2:latest",  # 👈 2.0 GB model (better quality)
            # model="llama3.2:1b",     # 👈 1.3 GB model (faster)
            temperature=0.7,
            num_predict=4096,
            base_url="http://localhost:11434"
        )
        
        async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
            await checkpointer.setup()
            
            config = {"configurable": {"thread_id": bot_id}}
            
            agent = create_agent(
                model=llm,
                tools=tools,
                checkpointer=checkpointer,
                system_prompt=system_prompt
            )
            
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]}, 
                config
            )
            
            messages = response.get("messages", [])
            
            if not messages:
                return {
                    "succeeded": False,
                    "message": "No response generated from agent."
                }
            
            final_response = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
            
            return {
                "succeeded": True,
                "response": final_response,
                "bot_id": bot_id
            }
            
    except Exception as e:
        return {
            "succeeded": False,
            "message": f"Query handling failed: {str(e)}"
        }