from app.graph.state import AgentState
from app.utils.logger import logger
from typing import Dict, Any

def handle_low_confidence(state: AgentState) -> Dict[str, Any]:
    logger.warning("Triggered low confidence breakpoint.")
    
    confidence = state.get("confidence_score", 0.0)
    retrieved_count = len(state.get("retrieved_docs", []))
    missing_context = state.get("missing_context", False)
    
    reason = "Undetermined reason."
    if retrieved_count == 0:
        reason = "No relevant internal documents were found to support the query."
    elif missing_context:
        reason = "The query covers topics not documented in our internal knowledge base."
    elif confidence < 0.70:
        reason = f"The analysis confidence ({int(confidence*100)}%) is below the required threshold (70%)."
        
    return {
        "summary_output": f"⚠️ ANALYSIS HALTED: {reason}\n\nPlease refine your query or upload relevant company documents.",
        "steps": ["confidence_breakpoint"]
    }
