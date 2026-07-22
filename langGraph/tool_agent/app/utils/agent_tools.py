import aiohttp 
from langchain_community.tools import DuckDuckGoSearchRun
# from app.services.pinecone_service import pine_
from langchain_core.tools import tool
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from app.core.config import settings
import os
from dotenv import load_dotenv
load_dotenv()


# embeddings = GoogleGenerativeAIEmbeddings(
#     model="gemini-embedding-001",
#     google_api_key="AIzaSyCJw443_VrCQ_8utfiu3FhViu7yn-ZL8k0",
#     task_type="retrieval_document",  
#     dimensions=768 
# )

class ToolsHandler:
    def __init__(self,index_name:str):
        self.index_name = index_name
        self.embeddings = OpenAIEmbeddings(model=settings.EMBEDDINGS_MODEL, api_key=settings.OPENAI_API_KEY)
        self.news_api_key = settings.NEWS_API_KEY


    async def get_info_from_pinecone(self,query: str) -> str:
        """
        Search the Pinecone vector database for relevant information based on the user's query.
        Args:
            query: The specific search term or question to look up in the knowledge base.
        """
        try:
            vec = pine_.retrieve_from_index_name(index_name=self.index_name, embeddings=self.embeddings)
            retriever = vec.as_retriever(search_type="similarity", search_kwargs={"k":2})
            docs = retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in docs])
            print(context)
            return context
        except Exception as e:
            return f"Error retrieving information: {str(e)}"

    async def web_search_tool(self,query: str) -> str:
        """
        Perform a web search to retrieve relevant information based on the user's query.
        Args:
            query: The specific search term or question to look up on the web.
        """
        try:
            search = DuckDuckGoSearchRun()
            result = search.invoke(query)
            print(f"Web search results for query '{query}': {result}")
            return result
        except Exception as e:
            print(f"Error performing web search for query '{query}': {str(e)}")
            return f"Error performing web search: {str(e)}"


    async def get_news_tool(self, query: str, max_results: int = 5) -> str:
            """
            Get the latest news articles based on a topic or keyword.
            
            Args:
                query: The topic to search for (e.g., "Pakistan economy")
                max_results: Number of articles to return (default: 5)
            
            Returns:
                Formatted string with news headlines, descriptions, and sources
            """
            try:
                if not self.news_api_key:
                    return "⚠️ News API key not configured. Please add NEWS_API_KEY to .env file."
                
                if not query:
                    return "❌ Please provide a topic to search for news."
                
                url = "https://gnews.io/api/v4/search"
                params = {
                    "q": query,
                    "token": self.news_api_key,
                    "lang": "en",
                    "country": "pk",
                    "max": max_results,
                    "sortby": "publishedAt"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status != 200:
                            return f"❌ News API error (Status {response.status})"
                        
                        data = await response.json()
                        
                        if not data.get("articles"):
                            return f"📭 No news found for '{query}'. Try a different topic."
                        
                        result = f"📰 **Latest News about '{query}':**\n\n"
                        
                        for i, article in enumerate(data["articles"][:max_results], 1):
                            title = article.get("title", "No title")
                            description = article.get("description", "No description")
                            source = article.get("source", {}).get("name", "Unknown")
                            url_link = article.get("url", "#")
                            published = article.get("publishedAt", "")
                            
                            if published:
                                try:
                                    from datetime import datetime
                                    pub_date = datetime.fromisoformat(published.replace("Z", "+00:00"))
                                    pub_date_str = pub_date.strftime("%B %d, %Y - %I:%M %p")
                                except:
                                    pub_date_str = published
                            else:
                                pub_date_str = "Unknown date"
                            
                            result += f"**{i}. {title}**\n"
                            result += f"   📝 {description}\n"
                            result += f"   📅 {pub_date_str}\n"
                            result += f"   🔗 Source: {source}\n"
                            result += f"   📎 {url_link}\n\n"
                        
                        return result
                        
            except aiohttp.ClientError as e:
                return f"❌ Network error: {str(e)}"
            except Exception as e:
                return f"❌ Error: {str(e)}"


system_prompt = """
you are Aswin gpt you are ai assistant for answering question based on the information provided by user and you have access to tool for searching information from interet and vector database.

always use first : get_info_from_pinecone : for searching information from vector database .
if not found information in vector database than use second  : web_search_tool : for searching information from web.
here is tool name : get_info_from_pinecone :
here is tool name : web_search_tool : for searching information from web
here is tool name : get_news_tool :  Get latest news on a topic
"""  