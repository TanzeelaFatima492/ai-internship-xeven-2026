from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone.vectorstores import Pinecone as PineconeVectorStore  # ✅ Sirf yeh rakhein
from fastapi import HTTPException
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()


pinecone_key = os.getenv("PINECONE_API_KEY")


class PineconeInsertRetrieval:
    def __init__(self, api_key):
        self.api_key = api_key

    # check index exists or not, create if missing
    def check_index(self, index_name,dimension=1536):
        """
        Check if index exists. If not, create it automatically.
        
        Args:
            index_name (str): Name of the index
            dimension (int): Dimension of embeddings (default: 1536 for text-embedding-ada-002)
            
        Returns:
            str: Status message
        """
        try:
            pc = Pinecone(api_key=self.api_key)
            indexes = pc.list_indexes().names()
            
            if index_name not in indexes:
                print(f"Index '{index_name}' not found. Creating new index...")
                self.create_index(index_name, dimension)
                return f"Index '{index_name}' created successfully with dimension {dimension}"
            else:
                return f"Index '{index_name}' already exists"
                
        except Exception as ex:
            return f"Error in check_index: {ex}"

    # create new index
    def create_index(self, index_name, dimentions):
        try:
            pc = Pinecone(api_key=self.api_key)
            pc.create_index(
                name=index_name,
                dimension=dimentions,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            print(f"Your index {index_name} created successfull")
            return index_name
        except Exception as ex:
            return f"sorry try again {ex}"

    # Delete Index Name
    def delete_index_name(self, index_name):
        try:
            pc = Pinecone(api_key=self.api_key)
            indexes = pc.list_indexes().names()
            if index_name not in indexes:
                return f"Index '{index_name}' does not exist."
            pc.delete_index(index_name)
            return f"Index '{index_name}' deleted successfully."
        except Exception as ex:
            return f"Failed to delete index '{index_name}': {ex}"

    # Delete NameSpace
    def delete_name_spaces(self, index_name, name_space):
        try:
            # Initialize the index
            pc = Pinecone(api_key=self.api_key)
            index = pc.Index(index_name)
            # Delete the namespace
            response = index.delete(namespace=name_space, delete_all=True)
            if response == {}:
                return f"Namespace '{name_space}' deleted successfully from index '{index_name}'."
            else:
                return f"Unexpected response: {response}"
        except Exception:
            return "An error occurred: Failed to Delete Namespace"

    # Create New nameSpace and insert Data in it
    async def insert_data_in_namespace(self, documents, embeddings, index_name, name_space):
        try:
            # Quick dimension check
            test_embedding = embeddings.embed_query("test")
            embedding_dim = len(test_embedding)
            
            # Get index info
            pc = Pinecone(api_key=self.api_key)
            index_info = pc.describe_index(index_name)
            index_dim = index_info.dimension
            
            if embedding_dim != index_dim:
                raise ValueError(f"Dimension mismatch: Embeddings have {embedding_dim} dimensions, index expects {index_dim}")
            
            doc_search = PineconeVectorStore.from_documents(
                documents, embeddings, index_name=index_name, namespace=name_space
            )
            print(f"Your Name space {name_space} is Created successfully")
            return doc_search
            
        except Exception as ex:
            return f"Failed to created namespace {ex}"

    # Insert Data in Index name
    def insert_data_in_index(self, documents, embeddings, index_name):
        try:
            PineconeVectorStore.from_documents(
                documents, embedding=embeddings, index_name=index_name
            )
            print(f"Your Data insert in {index_name} successfully")
        except Exception as ex:
            return f"Failed to created namespace {ex}"

    # Retrieve Data from index name
    def retrieve_from_index_name(self, index_name, embeddings):
        try:
            pc = Pinecone(api_key=self.api_key)
            index = pc.Index(index_name)
            vector_store = PineconeVectorStore(index=index, embedding=embeddings)
            return vector_store
        except Exception as ex:
            return f"Failed to load VectorStore {ex}"

    # Retrieve Data from Namespace
    async def retrieve_from_namespace(self,index_name,embeddings,name_space):
        try:
            # Initialize Pinecone client
            pc = Pinecone(api_key=self.api_key)
            
            # Get the index
            index = pc.Index(index_name)
            
            # Create and return the vector store object
            vectorstore = PineconeVectorStore(
                index=index,
                embedding=embeddings,
                namespace=name_space
            )
            
            return vectorstore
            
        except Exception as e:
            print(f"Error in retrieve_from_namespace: {e}")
            raise e
        

    def fetch_all_vectors(self, index_name: str) -> dict:
        """
        Fetches all vectors (IDs + values + metadata) for a serverless index using list + fetch.
        Note: index.fetch() always returns values and metadata by default.
        """
        namespace = "__default__"
        pc = Pinecone(api_key=self.api_key)
        idx = pc.Index(index_name)

        try:
            all_ids = []
            for batch in idx.list(namespace=namespace or None, limit=100):
                all_ids.extend(batch)

            result = {}
            for i in range(0, len(all_ids), 100):
                fetch_ids = all_ids[i : i + 100]
                resp = idx.fetch(ids=fetch_ids, namespace=namespace or None)
                result.update(resp.vectors)  # items include both 'values' and 'metadata'
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def list_indexes(self) -> List[str]:
        pc = Pinecone(api_key=self.api_key)
        return pc.list_indexes().names()
    

    def delete_by_id(self, index_name: str, vector_id: str) -> None:
        """
        Deletes a single vector from the specified index and namespace by its ID.
        """
        namespace = "__default__"
        idx = Pinecone(api_key=self.api_key).Index(index_name)
        try:
            idx.delete(ids=[vector_id], namespace=namespace or None)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    # Delete vectors by metadata filter
    async def delete_by_metadata_filter(self, index_name, namespace, metadata_filter):
        """
        Delete vectors from Pinecone index based on metadata filter
        
        Args:
            index_name (str): Name of the Pinecone index
            namespace (str): Namespace within the index
            metadata_filter (dict): Metadata filter to identify vectors to delete
            
        Returns:
            dict: Result of the delete operation
        """
        try:
            pc = Pinecone(api_key=self.api_key)
            index = pc.Index(index_name)
            
            # Delete vectors matching the metadata filter
            delete_response = index.delete(
                filter=metadata_filter,
                namespace=namespace
            )
            
            return {
                "status": "success",
                "message": f"Vectors deleted successfully from namespace '{namespace}'",
                "filter_used": metadata_filter,
                "response": delete_response
            }
            
        except Exception as ex:
            return {
                "status": "error",
                "message": f"Failed to delete vectors: {str(ex)}",
                "filter_used": metadata_filter
            }



pine_ = PineconeInsertRetrieval(pinecone_key)
