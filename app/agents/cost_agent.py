from app.services.llm_service import llm_service
from app.graph.state import AgentState
from typing import Dict, Any
from app.utils.logger import logger

class CostAnalysisAgent:
    def __init__(self):
        self.model = llm_service.get_model()

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Cost Analysis Agent processing...")
        query = state["query"]
        internal = state.get("internal_research", "")
        
        prompt = f"""
        You are a Financial and Infrastructure Cost Analyst.
        Evaluate the potential costs related to the following query.
        
        Query: {query}
        Internal Context: {internal}
        
        Analyze:
        - Implementation costs (staffing, tools)
        - Infrastructure impact (cloud, compute)
        - Ongoing maintenance requirements
        - Potential ROI or cost-saving opportunities
        """
        
        response = self.model.invoke(prompt)
        return {
            "cost_analysis": response.content,
            "steps": ["cost_agent"]
        }

cost_agent = CostAnalysisAgent()
