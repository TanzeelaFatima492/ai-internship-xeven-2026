from dotenv import load_dotenv
import os, time
from groq import Groq
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.llms import LLM
from langchain_classic.memory import ConversationBufferMemory
from typing import Optional, List

from calculator import calculator
from web_search_tool import web_search
from rag_tool import rag_search
from datetime_tool import get_current_datetime, calculate_date_difference
from performance_tracker import PerformanceTracker

load_dotenv()

# ---------- Performance Tracker ----------
tracker = PerformanceTracker()

# ---------- Custom Groq LLM with tracking ----------
class TrackedGroqLLM(LLM):
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0
    client: Optional[Groq] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        start = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                stop=stop
            )
            tracker.record_call("llm", True, time.time() - start)
            return response.choices[0].message.content
        except Exception as e:
            tracker.record_call("llm", False, time.time() - start)
            raise e

    @property
    def _llm_type(self) -> str:
        return "groq"

# ---------- LLM ----------
llm = TrackedGroqLLM(model="llama-3.1-8b-instant", temperature=0)

# ---------- Tools ----------
tools = [
    calculator,
    web_search,
    rag_search,
    get_current_datetime,
    calculate_date_difference
]

# ---------- ReAct Prompt ----------
prompt = PromptTemplate.from_template("""
You are a helpful AI research assistant with memory of our conversation.

You have access to the following tools:

{tools}

Available tool names: {tool_names}

Previous conversation:
{chat_history}

Use this format:
Question: the user's question
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: input for the tool
Observation: result from the tool
... (repeat as needed)
Thought: I now know the final answer
Final Answer: final answer to the user

Current Question: {input}
Thought: {agent_scratchpad}
""")

# ---------- Memory ----------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ---------- Agent ----------
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)