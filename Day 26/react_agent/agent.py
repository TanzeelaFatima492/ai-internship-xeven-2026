from dotenv import load_dotenv
import os
from groq import Groq
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.llms import LLM
from typing import Optional, List

from calculator import calculator
from web_search_tool import web_search
from rag_tool import rag_search

load_dotenv()

# ---------- Custom Groq LLM wrapper (no langchain-groq) ----------
class GroqLLM(LLM):
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0
    client: Optional[Groq] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            stop=stop
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        return "groq"

# ---------- LLM instance ----------
llm = GroqLLM(model="llama-3.1-8b-instant", temperature=0)

# ---------- Register tools ----------
tools = [calculator, web_search, rag_search]

# ---------- ReAct Prompt ----------
prompt = PromptTemplate.from_template("""
You are a helpful AI assistant.

You have access to the following tools:

{tools}

Available tool names:

{tool_names}

Use the following format:

Question: the question to answer

Thought: think about what to do

Action: one of [{tool_names}]

Action Input: input for the tool

Observation: result from the tool

... (repeat Thought/Action/Action Input/Observation as needed)

Thought: I now know the final answer

Final Answer: final response to the user

Question: {input}

Thought: {agent_scratchpad}
""")

# ---------- Create Agent ----------
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)