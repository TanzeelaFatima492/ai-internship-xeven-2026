from langchain_core.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."
        return "\n".join([f"- {r}" for r in results])
    except Exception as e:
        return f"Search error: {e}"