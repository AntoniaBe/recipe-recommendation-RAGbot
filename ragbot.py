from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from pineconeClient import PineConeClient
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
import constants


class RagBot:
    
    LLM_MODEL_NAME = "gpt-4o"

    EMBED_MODEL_NAME = "text-embedding-ada-002"

    def __init__(self) -> None:
        self.chat_engine = None
        self.index = None
        
        self.llm = OpenAI(model=self.LLM_MODEL_NAME, api_key=constants.OPENAI_API_KEY)

        self.embed_model = OpenAIEmbedding(model=self.EMBED_MODEL_NAME, api_key=constants.OPENAI_API_KEY)

        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 412
        Settings.chunk_overlap = 25
      
       
    def load(self):
        pinecone = PineConeClient()
        vector_count = pinecone.pinecone_info["total_vector_count"]

        if vector_count > 0:
                #print("Storage Not Empty. Loading from Database")
                self.index = VectorStoreIndex.from_vector_store(pinecone.vector_store)
        else:
                #print("Storage Empty. Loading Files to Database")
                reader = SimpleDirectoryReader(input_dir="data", recursive=True)
                docs = reader.load_data()
                storage_context = StorageContext.from_defaults(vector_store=pinecone.vector_store)
                self.index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

                 # add chat context, so it knows what you talked about before
                self.chat_engine = self.index.as_chat_engine(llm=self.llm, chat_mode="condense_question",
                                                     verbose=True)

    def query(self, question: str) -> str:
        response = self.query_engine.query(question)
        return response.response

    def chat(self, question: str, history: list = []) -> str:
        response = self.chat_engine.chat(question, chat_history=history)
        return response.response

