from app.rag.retriever import retriever
from app.services.llm_service import llm_service
from app.graph.state import AgentState
from typing import Dict, Any
from app.utils.logger import logger

class InternalResearchAgent:
    def __init__(self):
        self.model = llm_service.get_model()

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Internal Research Agent processing...")
        query = state["query"]
        
        # Retrieval
        docs = retriever.retrieve(query)
        retrieved_count = len(docs)
        
        # Log retrieval quality (Fix 3)
        logger.info(f"Retrieved chunks count: {retrieved_count}")
        retrieved_docs_info = []
        sources = set()
        for doc in docs:
            source = doc.metadata.get("source", "Unknown")
            logger.info(f"Retrieved document: {source}")
            retrieved_docs_info.append({
                "source": source,
                "content_preview": doc.page_content[:100] + "..."
            })
            sources.add(source)
        
        # RAG Validation (Fix 8)
        if retrieved_count == 0:
            logger.warning("No relevant internal documents found.")
            return {
                "internal_research": "No relevant internal documents found.",
                "retrieved_docs": [],
                "sources": [],
                "confidence_score": state.get("confidence_score", 0.9) - 0.25, # Initial reduction
                "steps": ["internal_research_agent"]
            }

        context = retriever.format_docs(docs)
        
        prompt = f"""
        You are an Internal Research Analyst. 
        Your task is to analyze internal company documents to answer the user's query.
        
        User Query: {query}
        
        Internal Documents Context:
        {context}
        
        Extract:
        - Relevant company policies
        - Constraints mentioned
        - Strategic objectives
        - Supporting evidence for decisions
        
        Be precise and cite the source if available.
        """
        
        response = self.model.invoke(prompt)
        
        # Limit to 3 sources for UI (Fix 4)
        top_sources = list(sources)[:3]
        
        return {
            "internal_research": response.content,
            "retrieved_docs": retrieved_docs_info,
            "sources": top_sources,
            "steps": ["internal_research_agent"]
        }

internal_research_agent = InternalResearchAgent()
