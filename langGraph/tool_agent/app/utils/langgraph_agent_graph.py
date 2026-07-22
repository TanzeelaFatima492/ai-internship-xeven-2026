
from langgraph.graph import StateGraph, END
from app.schema.schemas import AgentState
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from langgraph.checkpoint.memory import MemorySaver

from app.utils.nodes import web_search,out_of_scope_node,company_info,greet_node,intent_node
memory = MemorySaver()

def route_by_intent(state: AgentState) -> str:
    return state.get("intent", "out_of_scope")


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("intent", intent_node)
    graph.add_node("greet", greet_node)
    graph.add_node("company_info", company_info)
    graph.add_node("web_search", web_search)
    graph.add_node("out_of_scope", out_of_scope_node)

    graph.set_entry_point("intent")

    graph.add_conditional_edges(
        "intent",
        route_by_intent,
        {
            "greet": "greet",
            "web_search": "web_search",
            "company_info": "company_info",
            "out_of_scope": "out_of_scope",
        },
    )

    for node in ["greet", "company_info", "web_search", "out_of_scope"]:
        graph.add_edge(node, END)

    return graph.compile(checkpointer=memory)


agent = build_agent()



async def agent_handler(chatbot_schema):
    try:
        config = {"configurable": {"thread_id": chatbot_schema.bot_id}}
        result = agent.invoke({"user_query":chatbot_schema.query}, config=config)
        data=result["final_response"]
        message="Chat response generated successfully"
        return JSONResponse(
            content={
                "succeeded": "succeeded",
                "message": message,
                "httpStatusCode": 200,
                "data": jsonable_encoder(data)
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex :
        return JSONResponse(
            content={"succeeded": False, "message": str(ex)},
            status_code=500,
        )
        
        

