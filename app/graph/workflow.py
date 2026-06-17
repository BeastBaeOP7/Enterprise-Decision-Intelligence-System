from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.nodes import (
    query_node, profile_node, internal_research_node,
    external_research_node, cost_analysis_node, risk_analysis_node,
    debate_node, summary_node
)
from app.breakpoints.confidence_breakpoint import handle_low_confidence
from app.graph.edges import confidence_check

def create_workflow():
    # Initialize StateGraph with the state schema
    workflow = StateGraph(AgentState)

    # 1. Register Nodes
    workflow.add_node("query_agent", query_node)
    workflow.add_node("profile_agent", profile_node)
    workflow.add_node("internal_research", internal_research_node)
    workflow.add_node("external_research", external_research_node)
    workflow.add_node("cost_analysis", cost_analysis_node)
    workflow.add_node("risk_analysis", risk_analysis_node)
    workflow.add_node("debate_agent", debate_node)
    workflow.add_node("summary_agent", summary_node)
    workflow.add_node("low_confidence_handler", handle_low_confidence)

    # 2. Define Connectivity (Edges)
    
    # Entry point
    workflow.add_edge(START, "query_agent")
    
    # Sequential transition
    workflow.add_edge("query_agent", "profile_agent")
    
    # Parallel Fan-out: One source to multiple parallel nodes
    # In LangGraph V1, we can pass a list of targets
    # Parallel Fan-out
    workflow.add_edge("profile_agent", "internal_research")
    workflow.add_edge("profile_agent", "external_research")
    workflow.add_edge("profile_agent", "cost_analysis")
    workflow.add_edge("profile_agent", "risk_analysis") 

    # Fan-in: Multiple nodes converging to one
    workflow.add_edge("internal_research", "debate_agent")
    workflow.add_edge("external_research", "debate_agent")
    workflow.add_edge("cost_analysis", "debate_agent")
    workflow.add_edge("risk_analysis", "debate_agent")

    # Final Synthesis
    workflow.add_edge("debate_agent", "summary_agent")
    
    # Dynamic Breakpoint using Conditional Edge
    workflow.add_conditional_edges(
        "summary_agent",
        confidence_check,
        {
            "insufficient_confidence": "low_confidence_handler",
            "proceed": END
        }
    )
    
    workflow.add_edge("low_confidence_handler", END)
    return workflow.compile()

# Export the compiled workflow
app_workflow = create_workflow()
