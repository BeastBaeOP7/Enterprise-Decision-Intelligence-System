import os
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.rag.embeddings import get_embeddings
from app.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

class VectorStoreManager:
    def __init__(self, collection_name: str = "company_documents"):
        self.persist_directory = os.getenv("CHROMA_PATH", "./chroma_db")
        self.embeddings = get_embeddings()
        self.collection_name = collection_name
        self.vector_store = self._init_vector_store()

    def _init_vector_store(self):
        return Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents: List[Document]):
        logger.info(f"Adding {len(documents)} documents to ChromaDB collection: {self.collection_name}")
        self.vector_store.add_documents(documents)
        # Chroma in recent versions persists automatically or on cleanup
        
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k)

    def as_retriever(self, search_kwargs: dict = None):
        return self.vector_store.as_retriever(search_kwargs=search_kwargs or {"k": 5})

    def get_count(self) -> int:
        """Returns the number of documents in the collection."""
        try:
            return self.vector_store._collection.count()
        except Exception as e:
            logger.error(f"Error getting count for {self.collection_name}: {e}")
            return 0

vector_store_manager = VectorStoreManager()

