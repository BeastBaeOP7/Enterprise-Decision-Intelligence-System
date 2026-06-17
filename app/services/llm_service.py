import os
from typing import Optional, List, Dict, Any
from langchain_openai import ChatOpenAI
from app.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self, model_name: Optional[str] = None):
        self.api_key = os.getenv("GITHUB_TOKEN")
        self.base_url = os.getenv("BASE_URL", "https://models.inference.ai.azure.com")
        self.model_name = model_name or os.getenv("GITHUB_MODEL", "gpt-4o-mini")
        
        if not self.api_key:
            logger.warning("GITHUB_TOKEN not found in environment variables.")

    def get_model(self, temperature: float = 0.7, **kwargs):
        """Returns a LangChain ChatOpenAI object configured for GitHub Models."""
        return ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model_name,
            temperature=temperature,
            **kwargs
        )

    def call_model(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Direct call to the model with messages."""
        try:
            model = self.get_model(temperature=temperature)
            response = model.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            return f"Error: {str(e)}"

llm_service = LLMService()
