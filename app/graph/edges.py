from langgraph.graph import END
from app.graph.state import AgentState
from app.utils.logger import logger

def confidence_check(state: AgentState) -> str:
    """
    Decides whether to proceed to final report or trigger low confidence handler.
    """
    confidence = state.get("confidence_score", 0.0)
    retrieved_count = len(state.get("retrieved_docs", []))
    missing_context = state.get("missing_context", False)
    
    logger.info(f"Edge Check - Confidence: {confidence}, Docs: {retrieved_count}, Missing Context: {missing_context}")
    
    # Real Breakpoint Logic (Fix 2)
    if confidence < 0.70 or retrieved_count == 0 or missing_context:
        return "insufficient_confidence"
    return "proceed"

def missing_context_check(state: AgentState) -> str:
    """
    Checks if query agent flagged missing context.
    """
    if state.get("missing_context", False):
        return "missing_context"
    return "context_complete"
