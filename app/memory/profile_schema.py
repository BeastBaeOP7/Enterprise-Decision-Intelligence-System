from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfile(BaseModel):
    user_id: str
    name: str = "Default User"
    role: str = "Business Analyst"
    expertise: str = "Intermediate"
    preferred_output: str = "Executive Summary"
    research_history: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    expertise: Optional[str] = None
    preferred_output: Optional[str] = None
    interests: Optional[List[str]] = None
