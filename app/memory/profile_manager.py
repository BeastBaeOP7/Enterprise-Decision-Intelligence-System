import json
import os
from typing import Dict, Optional
from app.memory.profile_schema import UserProfile
from app.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

class ProfileManager:
    def __init__(self):
        self.file_path = os.getenv("USER_PROFILES_PATH", "data/user_profiles/profiles.json")
        self.profiles: Dict[str, UserProfile] = self._load_profiles()

    def _load_profiles(self) -> Dict[str, UserProfile]:
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return {k: UserProfile(**v) for k, v in data.items()}
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
            return {}

    def save_profiles(self):
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump({k: v.model_dump() for k, v in self.profiles.items()}, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving profiles: {e}")

    def get_profile(self, user_id: str) -> UserProfile:
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(user_id=user_id)
            self.save_profiles()
        return self.profiles[user_id]

    def update_profile(self, user_id: str, updates: dict):
        profile = self.get_profile(user_id)
        for key, value in updates.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        self.save_profiles()

profile_manager = ProfileManager()
