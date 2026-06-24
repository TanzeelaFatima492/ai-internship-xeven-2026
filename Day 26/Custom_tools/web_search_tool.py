from langchain.tools import tool
from duckduckgo_search import DDGS


@tool
def web_search(query: str) -> str:
    """
    Search the web and return summarized results.

    Args:
        query: Search query.

    Returns:
        Search results summary.
    """
    try:
        results = DDGS().text(query, max_results=5)

        summaries = []

        for index, result in enumerate(results, start=1):
            summaries.append(
                f"{index}. {result['title']}\n"
                f"{result['body']}\n"
            )

        if not summaries:
            return "No results found."

        return "\n".join(summaries)

    except Exception as e:
        return f"Search Error: {str(e)}"


if __name__ == "__main__":
    query = input("Enter search query: ")
    print(web_search.invoke(query))