from typing import Dict, Any
from app.services.llm_service import llm_service
from app.graph.state import AgentState
import json
from app.utils.logger import logger

class QueryAgent:
    def __init__(self):
        self.model = llm_service.get_model(temperature=0)

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Query Agent processing...")
        query = state["query"]
        
        prompt = f"""
        Analyze the following user query for enterprise decision support.
        Classify the intent, domain, and complexity.
        
        Also, determine if the query is about a highly speculative or likely unknown topic for the company (e.g. acquiring major external companies like SpaceX, entering entirely new industries like quantum computing or nuclear power).
        
        Query: {query}
        
        Return ONLY a JSON object with:
        - intent (e.g., technology_comparison, budget_analysis, policy_inquiry)
        - domain (e.g., ai_frameworks, cloud_computing, security)
        - complexity (low, medium, high)
        - is_unknown_topic (boolean)
        """
        
        response = self.model.invoke(prompt)
        try:
            content = response.content.strip()
            # Handle potential markdown blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            metadata = json.loads(content)
            return {
                "intent": metadata.get("intent", "generic"),
                "domain": metadata.get("domain", "general"),
                "complexity": metadata.get("complexity", "medium"),
                "missing_context": metadata.get("is_unknown_topic", False), # Map to missing_context for breakpoint
                "steps": ["query_agent"]
            }
        except Exception as e:
            logger.error(f"Error in QueryAgent: {e}")
            return {
                "intent": "generic",
                "domain": "general",
                "complexity": "medium",
                "steps": ["query_agent_fallback"]
            }

query_agent = QueryAgent()
