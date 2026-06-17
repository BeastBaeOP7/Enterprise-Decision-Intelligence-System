from app.memory.profile_manager import profile_manager
from app.graph.state import AgentState
from typing import Dict, Any
from app.utils.logger import logger
from app.services.llm_service import llm_service

class ProfileAgent:
    def __init__(self):
        self.model = llm_service.get_model()

    def process(self, state: AgentState) -> Dict[str, Any]:
        logger.info("Profile Agent processing...")
        user_id = state.get("user_id", "default")
        query = state.get("query", "")
        current_profile = profile_manager.get_profile(user_id)
        
        # Inference Prompt
        prompt = f"""
        Analyze the user's query and existing profile to infer the most likely temporary persona for this interaction.
        
        Available Profiles:
        - Business Analyst
        - CFO
        - Engineering Manager
        - Security Officer
        - Operations Manager
        
        User Query: {query}
        Current Role: {current_profile.role}
        
        Choose the most relevant profile from the list above. If unsure, default to 'Business Analyst'.
        Return ONLY the profile name.
        """
        
        response = self.model.invoke(prompt)
        inferred_role = response.content.strip()
        
        # Validate inferred role
        valid_roles = ["Business Analyst", "CFO", "Engineering Manager", "Security Officer", "Operations Manager"]
        if inferred_role not in valid_roles:
             # Try to find if any valid role is in the string
             found = False
             for v in valid_roles:
                 if v.lower() in inferred_role.lower():
                     inferred_role = v
                     found = True
                     break
             if not found:
                 inferred_role = current_profile.role if current_profile.role in valid_roles else "Business Analyst"

        logger.info(f"Inferred User Profile: {inferred_role}")
        
        # Update profile for this interaction
        updated_profile_dict = current_profile.model_dump()
        updated_profile_dict["role"] = inferred_role
        
        return {
            "user_profile": updated_profile_dict,
            "steps": ["profile_agent"]
        }

profile_agent = ProfileAgent()
