from typing import List, Dict, Any
from app.utils.logger import logger

class SearchService:
    """
    Mock search service for external research.
    Future integration: Tavily, Serper, Google Search API.
    """
    def search(self, query: str) -> List[Dict[str, Any]]:
        logger.info(f"External search triggered for: {query}")
        # Return mock results for MVP
        return [
            {
                "title": f"Recent trends in {query}",
                "snippet": f"Industry reports suggest that {query} is seeing rapid adoption across enterprise sectors in 2024.",
                "link": "https://example.com/trends"
            }
        ]

search_service = SearchService()
