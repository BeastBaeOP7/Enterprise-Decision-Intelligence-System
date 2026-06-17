from typing import Dict, Any
from app.agents.query_agent import query_agent
from app.agents.profile_agent import profile_agent
from app.agents.internal_research_agent import internal_research_agent
from app.agents.external_research_agent import external_research_agent
from app.agents.cost_agent import cost_agent
from app.agents.risk_agent import risk_agent
from app.agents.debate_agent import debate_agent
from app.agents.summary_agent import summary_agent
from app.graph.state import AgentState

import time
from datetime import datetime

def wrap_node(node_func, name):
    def wrapper(state: AgentState) -> Dict[str, Any]:
        start_time = time.time()
        start_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        result = node_func(state)
        
        end_time = time.time()
        end_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        duration = round(end_time - start_time, 2)
        
        # Ensure result is a dict and add execution log
        if not isinstance(result, dict):
            result = {}
            
        result["execution_logs"] = [{
            "agent": name,
            "start": start_str,
            "end": end_str,
            "duration": duration,
            "timestamp": start_time
        }]
        return result
    return wrapper

def query_node(state: AgentState) -> Dict[str, Any]:
    return wrap_node(query_agent.process, "Query Agent")(state)

def profile_node(state: AgentState) -> Dict[str, Any]:
    return wrap_node(profile_agent.process, "Profile Agent")(state)

def internal_research_node(state: AgentState) -> Dict[str, Any]:
    # Simulate some work for visualization
    time.sleep(1.5)
    return wrap_node(internal_research_agent.process, "Research Agent")(state)

def external_research_node(state: AgentState) -> Dict[str, Any]:
    time.sleep(1.2)
    return wrap_node(external_research_agent.process, "External Research Agent")(state)

def cost_analysis_node(state: AgentState) -> Dict[str, Any]:
    time.sleep(0.8)
    return wrap_node(cost_agent.process, "Cost Agent")(state)

def risk_analysis_node(state: AgentState) -> Dict[str, Any]:
    time.sleep(1.0)
    return wrap_node(risk_agent.process, "Risk Agent")(state)

def debate_node(state: AgentState) -> Dict[str, Any]:
    return wrap_node(debate_agent.process, "Debate Agent")(state)

def summary_node(state: AgentState) -> Dict[str, Any]:
    return wrap_node(summary_agent.process, "Summary Agent")(state)
