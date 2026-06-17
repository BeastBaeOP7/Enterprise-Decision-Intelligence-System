from app.services.llm_service import llm_service
from app.graph.state import AgentState
from typing import Dict, Any
from app.utils.logger import logger

class ExternalResearchAgent:
    def __init__(self):
        self.model = llm_service.get_model()

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("External Research Agent processing...")
        query = state["query"]
        
        prompt = f"""
        You are an External Market Researcher.
        Yoar task is to provide industry trends, technical best practices, and framework comparisons related to the user's query.
        
        User Query: {query}
        
        Provide a detailed analysis based on current industry knowledge (up to early 2024).
        Focus on:
        - Technology maturity
        - Industry standard adoption
        - Comparison with alternatives
        """
        
        response = self.model.invoke(prompt)
        return {
            "external_research": response.content,
            "steps": ["external_research_agent"]
        }

external_research_agent = ExternalResearchAgent()
