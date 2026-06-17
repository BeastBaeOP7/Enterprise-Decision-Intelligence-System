from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str
    user_id: str = "user_001"

class QueryResponse(BaseModel):
    result: str
    confidence_score: float
    steps: List[str]
    execution_logs: List[Dict[str, Any]]
    user_profile: Dict[str, Any]
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
