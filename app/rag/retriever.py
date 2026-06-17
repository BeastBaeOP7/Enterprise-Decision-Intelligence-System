from typing import List
from langchain_core.documents import Document
from app.rag.vector_store import vector_store_manager
from app.utils.logger import logger

class EnterpriseRetriever:
    def __init__(self):
        self.vector_store = vector_store_manager

    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        logger.info(f"Retrieving documents for query: {query}")
        return self.vector_store.similarity_search(query, k=k)

    def format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join(f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}" for doc in docs)

retriever = EnterpriseRetriever()
