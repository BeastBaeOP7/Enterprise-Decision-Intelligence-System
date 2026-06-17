import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
COMPANY_DOCS_DIR = os.path.join(DATA_DIR, "company_docs")
USER_PROFILES_PATH = os.path.join(DATA_DIR, "user_profiles", "profiles.json")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# Agent Config
CONFIDENCE_THRESHOLD = 0.70
MAX_RETRIEVAL_CHUNKS = 5

# Model Config
LLM_TEMPERATURE = 0.7
SUMMARY_TEMPERATURE = 0.3
