from app.services.llm_service import llm_service
from app.graph.state import AgentState
from typing import Dict, Any
from app.utils.logger import logger

class DebateAgent:
    def __init__(self):
        self.model = llm_service.get_model()

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Debate Agent processing...")
        internal = state.get("internal_research", "")
        external = state.get("external_research", "")
        cost = state.get("cost_analysis", "")
        risk = state.get("risk_analysis", "")
        
        prompt = f"""
        You are a Strategic Decision Architect. 
        Your task is to synthesize findings from different analysts and identify conflicts or trade-offs.
        
        INTERNAL RESEARCH:
        {internal}
        
        EXTERNAL RESEARCH:
        {external}
        
        COST ANALYSIS:
        {cost}
        
        RISK ANALYSIS:
        {risk}
        
        Tasks:
        1. CONTRADICTIONS: Where do internal policy and external trends/market options disagree?
        2. TRADE-OFFS: What are the primary balances between cost, risk, and strategic value?
        3. AREAS OF UNCERTAINTY: What is still unknown?
        4. CONSENSUS: Based on all analyses, what is the level of agreement (0-100%)?
        
        Provide your analysis. 
        IMPORTANT: Your last line MUST be exactly: "CONSENSUS_SCORE: X" where X is a number between 0 and 100.
        """
        
        response = self.model.invoke(prompt)
        content = response.content
        
        # Parse consensus score
        consensus_score = 0.75 # Default fallback
        try:
            import re
            match = re.search(r"CONSENSUS_SCORE:\s*(\d+)", content)
            if match:
                consensus_score = float(match.group(1)) / 100.0
        except Exception as e:
            logger.error(f"Error parsing consensus score: {e}")

        return {
            "debate_output": content,
            "consensus_score": consensus_score,
            "steps": ["debate_agent"]
        }

debate_agent = DebateAgent()
