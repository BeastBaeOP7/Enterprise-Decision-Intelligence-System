from typing import List, Dict, Any
from app.rag.vector_store import VectorStoreManager
from langchain_core.documents import Document
from app.utils.logger import logger

class MemoryStore:
    def __init__(self):
        self.vector_store = VectorStoreManager(collection_name="conversation_memory")

    def add_interaction(self, user_id: str, query: str, result: str):
        doc = Document(
            page_content=f"Query: {query}\nResult: {result}",
            metadata={"user_id": user_id, "type": "interaction"}
        )
        self.vector_store.add_documents([doc])
        logger.info(f"Added interaction memory for user {user_id}")

    def get_relevant_memories(self, user_id: str, query: str, k: int = 3) -> List[Document]:
        # Filter for user_id - Note: LangChain Chroma support for metadata filtering
        # For simplicity in MVP, we'll just search and format
        return self.vector_store.similarity_search(query, k=k)

memory_store = MemoryStore()
