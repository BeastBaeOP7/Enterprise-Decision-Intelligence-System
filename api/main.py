from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from api.schemas import QueryRequest, QueryResponse, HealthResponse
from app.graph.workflow import app_workflow
from app.rag.document_loader import DocumentLoader
from app.rag.chunker import DocumentChunker
from app.rag.vector_store import vector_store_manager
from app.utils.logger import logger
import os
import uuid

app = FastAPI(title="EDIS API")

@app.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    logger.info(f"Received query: {request.query}")
    
    # In V1, we use a config with thread_id for checkpointing support
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "query": request.query,
        "user_id": request.user_id,
        "steps": [],
        "execution_logs": [],
        "internal_research": "",
        "external_research": "",
        "cost_analysis": "",
        "risk_analysis": "",
        "debate_output": "",
        "summary_output": "",
        "confidence_score": 0.0,
        "consensus_score": 1.0,
        "missing_context": False,
        "context_request": "",
        "retrieved_docs": [],
        "sources": []
    }
    
    try:
        # ainvoke in LangGraph V1 takes state and config
        final_state = await app_workflow.ainvoke(initial_state, config=config)
        
        # Update memory store (manual)
        try:
            from app.memory.memory_store import memory_store
            memory_store.add_interaction(
                request.user_id, 
                request.query, 
                final_state.get("summary_output", "No summary generated")
            )
        except Exception as e:
            logger.error(f"Failed to save to memory: {e}")
        
        return {
            "result": final_state.get("summary_output", "Analysis failed"),
            "confidence_score": final_state.get("confidence_score", 0.0),
            "steps": final_state.get("steps", []),
            "execution_logs": final_state.get("execution_logs", []),
            "user_profile": final_state.get("user_profile", {}),
            "metadata": {
                "intent": final_state.get("intent", "unknown"),
                "domain": final_state.get("domain", "unknown"),
                "thread_id": thread_id
            }
        }
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        return {
            "result": f"Error during analysis: {str(e)}",
            "confidence_score": 0.0,
            "steps": ["error"],
            "debate": "N/A",
            "metadata": {"error": str(e)}
        }

@app.on_event("startup")
async def startup_event():
    """
    Automatically index company documents if the collection is empty.
    """
    try:
        count = vector_store_manager.get_count()
        if count == 0:
            logger.info("Company documents collection is empty. Starting automatic indexing...")
            reindex_documents()
        else:
            logger.info(f"company_documents already contains {count} vectors. Skipping re-index.")
    except Exception as e:
        logger.error(f"Startup indexing failed: {e}")

@app.get("/debug/vector-store")
async def debug_vector_store():
    """
    Returns the counts of both company_documents and conversation_memory collections.
    """
    try:
        from app.memory.memory_store import memory_store
        company_count = vector_store_manager.get_count()
        memory_count = memory_store.vector_store.get_count()
        
        return {
            "company_documents_count": company_count,
            "conversation_memory_count": memory_count
        }
    except Exception as e:
        logger.error(f"Debug endpoint failed: {e}")
        return {"error": str(e)}

@app.post("/upload-documents")
async def upload_documents(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    # Save files to company_docs
    upload_dir = os.getenv("COMPANY_DOCS_PATH", "./data/company_docs")
    os.makedirs(upload_dir, exist_ok=True)
    
    saved_paths = []
    for file in files:
        path = os.path.join(upload_dir, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        saved_paths.append(path)
    
    # Schedule background indexing
    background_tasks.add_task(reindex_documents)
    
    return {"message": f"Uploaded {len(files)} files. Indexing started in background."}

def reindex_documents():
    try:
        logger.info("Starting indexing process...")
        loader = DocumentLoader(os.getenv("COMPANY_DOCS_PATH", "./data/company_docs"))
        chunker = DocumentChunker()
        
        docs = loader.load_documents()
        doc_count = len(docs)
        logger.info(f"Loaded {doc_count} company documents.")
        
        if docs:
            chunks = chunker.split_documents(docs)
            chunk_count = len(chunks)
            logger.info(f"Generated {chunk_count} chunks.")
            
            vector_store_manager.add_documents(chunks)
            logger.info(f"Indexed {chunk_count} vectors into company_documents.")
        else:
            logger.warning("No documents found to index.")
            
        logger.info("Indexing complete.")
    except Exception as e:
        logger.error(f"Indexing failed: {e}")
