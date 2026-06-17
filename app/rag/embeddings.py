from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embeddings():
    model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    return HuggingFaceEmbeddings(model_name=model_name)
