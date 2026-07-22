from email import message

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.schema.schemas import AgentState
from app.utils.agent_prompt import INTENT_PROMPT,GREET_PROMPT
from app.core.config import settings
import json
from langchain_community.tools import DuckDuckGoSearchRun


def intent_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )
    response = llm.invoke([
        SystemMessage(content=INTENT_PROMPT),
        HumanMessage(content=state["user_query"]),
    ])
    try:
        result = json.loads(response.content.strip())
        intent = result.get("intent", "out_of_scope")
    except (json.JSONDecodeError, AttributeError):
        intent = "out_of_scope"

    valid_intents = {"web_search", "company_info", "greet", "out_of_scope"}
    if intent not in valid_intents:
        intent = "out_of_scope"

    return {**state, "intent": intent}



def greet_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0.7,
    )
    response = llm.invoke([
        SystemMessage(content=GREET_PROMPT),
        HumanMessage(content=state["user_query"]),
    ])
    return {**state, "final_response": response.content.strip()}


def company_info(state: AgentState) -> AgentState:
    company_info = """Xeven solution is tech company in pakistan , they have 200 employees 
    they are working in ai in health care domain here is official website name xevensolutions.com"""
    return {**state, "final_response": company_info}


def web_search(state: AgentState) -> AgentState:
        """
        Perform a web search to retrieve relevant information based on the user's query.
        Args:
            query: The specific search term or question to look up on the web.
        """
        try:
            search = DuckDuckGoSearchRun()
            result = search.invoke(state["user_query"])
            print(f"Web search results for query '{state["user_query"]}': {result}")
            return {**state, "final_response": result}
        except Exception as e:
            print(f"Error performing web search for query '{state["user_query"]}': {str(e)}")
            return {**state, "final_response": f"Error performing web search: {str(e)}"}
        
        
def out_of_scope_node(state: AgentState) -> AgentState:
    message = (
        "Sorry, I can only help you with:\n"
        "  • Web search \n"
        "  • About company information \n\n"
        "Please ask me something related to these topics    !"
    )
    return {**state, "final_response": message}