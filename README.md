# Enterprise Decision Intelligence System (EDIS)

EDIS is a production-quality Multi-Agent Decision Support system built for enterprise analysts. It leverages LangGraph for parallel agent orchestration and GitHub Models for high-performance reasoning.

## Features
- **Multi-Agent Collaboration**: Query, Profile, Internal/External Research, Cost, Risk, Debate, and Summary agents.
- **LangGraph Parallel Execution**: Efficiently gathers data from multiple perspectives in parallel.
- **RAG Integration**: Analyzes internal company documents using ChromaDB and local HuggingFace embeddings.
- **Debate-Based Reasoning**: Explicitly identifies conflicts between internal policy and external trends.
- **User Memory**: Tracks user profiles and research history for personalized support.
- **Dynamic Breakpoints**: Intelligent interruptions for low-confidence results.

## Tech Stack
- **Backend**: FastAPI, LangGraph, ChromaDB
- **Frontend**: Streamlit
- **LLM**: GitHub Models (OpenAI compatible)
- **Embeddings**: HuggingFace (Local)

## Getting Started

### 1. Prerequisites
- Python 3.10+
- GitHub Token with access to GitHub Models Marketplace

### 2. Setup
```bash
# Clone the repository (if applicable)
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env # Edit .env with your GITHUB_TOKEN
```

### 3. Run the Application
```bash
python run.py
```
This will start both the FastAPI backend (port 8000) and the Streamlit frontend.

### 4. Upload Documents
Use the Streamlit sidebar to upload text or PDF documents to the `data/company_docs/` folder and trigger re-indexing.

## Project Structure
- `api/`: FastAPI routes and schemas.
- `app/agents/`: specialized agent logic.
- `app/graph/`: LangGraph workflow definition.
- `app/rag/`: Document loading, chunking, and vector store management.
- `frontend/`: Streamlit dashboard code.
- `data/`: Local storage for documents, profiles, and reports.
