from typing import Annotated, List, Dict, Any, TypedDict
import operator

def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return {**a, **b}

class AgentState(TypedDict):
    # The original user message
    query: str
    user_id: str
    
    # Metadata from Query Agent
    intent: str
    domain: str
    complexity: str
    
    # User Profile from Profile Agent
    user_profile: Dict[str, Any]
    
    # Findings from parallel agents
    internal_research: str
    external_research: str
    cost_analysis: str
    risk_analysis: str
    
    # Results from synthesis agents
    debate_output: str
    summary_output: str
    
    # Final combined report
    final_report: Dict[str, Any]
    
    # Execution tracking - Using Annotated with operator.add for accumulation
    steps: Annotated[List[str], operator.add]
    execution_logs: Annotated[List[Dict[str, Any]], operator.add]
    
    # Confidence and Context
    confidence_score: float
    consensus_score: float
    missing_context: bool
    context_request: str
    
    # Retrieval verification
    retrieved_docs: List[Dict[str, Any]]
    sources: List[str]

