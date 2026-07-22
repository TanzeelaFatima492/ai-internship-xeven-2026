from langchain_community.tools import DuckDuckGoSearchRun

async def web_search_tool(query: str) -> str:
    """Search internet for information"""
    try:
        search = DuckDuckGoSearchRun()
        return search.invoke(query)
    except Exception as e:
        return f"Web search failed: {str(e)}"