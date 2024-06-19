from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
import constants


pinecone_api_key = constants.PINECONE_API_KEY


class PineConeClient:
    def __init__(self) -> None:
        pc = Pinecone(pinecone_api_key)

        # Create a new index if it doesn't exist
        index_name = "recipes"
        if index_name not in pc.list_indexes().names():
            pc.create_index(
            name=index_name,
            dimension=1536, 
            metric="cosine", 
            spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
    ) 
        self.pinecone_index = pc.Index(index_name)
        self.pinecone_info =  self.pinecone_index.describe_index_stats()
        self.vector_store = PineconeVectorStore(pinecone_index=self.pinecone_index)


    







