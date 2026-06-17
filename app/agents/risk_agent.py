from app.services.llm_service import llm_service
from app.graph.state import AgentState
from typing import Dict, Any
from app.utils.logger import logger

class RiskAnalysisAgent:
    def __init__(self):
        self.model = llm_service.get_model()

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Risk Analysis Agent processing...")
        query = state["query"]
        internal = state.get("internal_research", "")
        
        prompt = f"""
        You are a Risk and Compliance Officer.
        Identify potential risks related to the following query.
        
        Query: {query}
        Internal Context: {internal}
        
        Analyze:
        - Security risks (data privacy, vulnerabilities)
        - Compliance risks (regulatory, internal policy)
        - Operational risks (adoption, technical debt)
        - Strategic risks (vendor lock-in)
        """
        
        response = self.model.invoke(prompt)
        return {
            "risk_analysis": response.content,
            "steps": ["risk_agent"]
        }

risk_agent = RiskAnalysisAgent()
