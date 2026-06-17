import os
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, DirectoryLoader
from langchain_core.documents import Document
from app.utils.logger import logger

class DocumentLoader:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def load_documents(self) -> List[Document]:
        if not os.path.exists(self.directory_path):
            logger.warning(f"Directory {self.directory_path} does not exist.")
            return []
        
        logger.info(f"Loading documents from {self.directory_path}")
        
        # Loader for PDFs
        pdf_loader = DirectoryLoader(
            self.directory_path,
            glob="**/*.pdf",
            loader_cls=PyMuPDFLoader
        )
        
        # Loader for TXT
        txt_loader = DirectoryLoader(
            self.directory_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        
        docs = pdf_loader.load() + txt_loader.load()
        logger.info(f"Loaded {len(docs)} documents.")
        return docs
