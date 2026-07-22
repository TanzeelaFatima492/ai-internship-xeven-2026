from fastapi import APIRouter, status, UploadFile, File , Depends
from typing import Optional
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile , os
from langchain_core.documents import Document
from app.schema.schemas import ChatRequestAgent,LanggraphAgentRequest
from app.services.pinecone_service import pine_
from app.db.autherization import JWTBearer
from app.utils.utils import handle_query
from app.utils.langgraph_agent_graph import agent_handler
load_dotenv()
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings

embedding = OpenAIEmbeddings(model="text-embedding-3-small",api_key=os.getenv("OPENAI_API_KEY"))

# embeddings = GoogleGenerativeAIEmbeddings(
#     model="gemini-embedding-001",
#     google_api_key="AIzaSyCJw443_VrCQ_8utfiu3FhViu7yn-ZL8k0",
#     task_type="retrieval_document",  
#     dimensions=768 
# )

chatbot_router = APIRouter()


@chatbot_router.post("/chatbot-agent", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def handle_query_endpoint(chatbot_schema:ChatRequestAgent):
    result = await handle_query(chatbot_schema)
    return result


@chatbot_router.post("/langgraph-agent", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def handle_query_endpoint(chatbot_schema:LanggraphAgentRequest):
    result = await agent_handler(chatbot_schema)
    return result


@chatbot_router.post("/ingest-data", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def ingest_data_endpoint(
    pdf_file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = None,
    index_name: str = ""
):
    """
    Endpoint to ingest PDF files or text content into Pinecone.
    
    Args:
        index_name: Name of the Pinecone index
        pdf_file: Optional PDF file to upload
        text_content: Optional text content to ingest
        
    Returns:
        dict: Status and logs of the ingestion process
    """
    logs = []
    
    try:
        # Validate input
        if not pdf_file and not text_content:
            return {
                "succeeded": False,
                "message": "Either PDF file or text content must be provided",
                "logs": logs
            }
        
        documents = []
        
        # Handle PDF file
        if pdf_file:
            logs.append(f"Starting PDF processing for file: {pdf_file.filename}")
            temp_file_path = None
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file_path = temp_file.name
                    # Save uploaded file to temp location
                    contents = await pdf_file.read()
                    with open(temp_file_path, "wb") as f:
                        f.write(contents)
                    logs.append(f"Temporary PDF file created: {temp_file_path}")
                
                # Load PDF using PyMuPDFLoader
                loader = PyMuPDFLoader(temp_file_path)
                documents = loader.load()
                logs.append(f"PDF loaded successfully. Total pages/documents: {len(documents)}")
                
                # Explicitly delete loader to release file handle
                del loader
                
                # Clean up temp file with retry logic
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.remove(temp_file_path)
                        logs.append(f"Temporary PDF file deleted: {temp_file_path}")
                    except Exception as cleanup_error:
                        logs.append(f"Warning: Could not delete temporary file: {str(cleanup_error)}")
                
            except Exception as e:
                logs.append(f"Error processing PDF: {str(e)}")
                # Try to cleanup on error
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.remove(temp_file_path)
                    except:
                        pass
                return {
                    "succeeded": False,
                    "message": f"PDF processing failed: {str(e)}",
                    "logs": logs
                }
        
        # Handle text content
        if text_content:
            logs.append("Processing text content")
            text_doc = Document(page_content=text_content, metadata={"source": "text_input"})
            documents.append(text_doc)
            logs.append("Text content added to documents")
        
        # Split documents using RecursiveCharacterTextSplitter
        logs.append("Starting document splitting with RecursiveCharacterTextSplitter")
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4o-mini",
            chunk_size=1500,
            chunk_overlap=100
        )
        
        split_documents = splitter.split_documents(documents)
        logs.append(f"Documents split successfully. Total chunks: {len(split_documents)}")
        
        # Check if index exists
        logs.append(f"Checking if index '{index_name}' exists...")
        check_result = pine_.check_index(index_name, dimension=1536)
        logs.append(f"Index check result: {check_result}")
        
        # Delete existing index to add fresh data
        logs.append(f"Deleting existing index '{index_name}' for fresh data ingestion...")
        delete_result = pine_.delete_index_name(index_name)
        logs.append(f"Index deletion result: {delete_result}")
        
        # Check and create index again
        logs.append(f"Creating fresh index '{index_name}'...")
        recreate_result = pine_.check_index(index_name, dimension=1536)
        logs.append(f"Index recreation result: {recreate_result}")
        
        # Insert data into the index
        logs.append(f"Inserting {len(split_documents)} chunks into index '{index_name}'...")
        insert_result = pine_.insert_data_in_index(
            documents=split_documents,
            embeddings=embedding,
            index_name=index_name
        )
        logs.append(f"Data insertion result: {insert_result}")
        
        logs.append("Data ingestion completed successfully")
        
        return {
            "succeeded": True,
            "message": f"Successfully ingested {len(split_documents)} document chunks into index '{index_name}'",
            "chunks_created": len(split_documents),
            "logs": logs
        }
        
    except Exception as e:
        logs.append(f"Unexpected error during ingestion: {str(e)}")
        return {
            "succeeded": False,
            "message": f"Data ingestion failed: {str(e)}",
            "logs": logs
        }

