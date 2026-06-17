import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Decision Intelligence Assistant",
    page_icon="🧠",
    layout="centered"
)

API_URL = "http://localhost:8000"

# Header
st.title("🧠 Multi-Agent Decision Intelligence Assistant")
st.markdown("##### Powered by Parallel Agent Execution using LangGraph")
st.divider()

# Initialize chat history with structured metadata
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    user_id = st.text_input("User ID", value="gautham")
    
    st.divider()
    st.subheader("📊 Session Stats")
    if st.session_state.messages:
        total_queries = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Questions Asked", total_queries)
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display metadata if it exists
        if "metadata" in message:
            meta = message["metadata"]
            
            # Badges Row
            cols = st.columns(4)
            cols[0].metric("🧠 Profile Detected", meta["profile_role"])
            cols[1].metric("⚡ Parallel Gain", f"{meta['speedup']:.1f}x")
            cols[2].metric("🎯 Confidence", meta["confidence"])
            cols[3].metric("🛑 Breakpoint", meta["breakpoint"])
            
            # Parallel Agents
            st.markdown("**Core Analysis Tracks:**")
            agent_cols = st.columns(4)
            parallel_labels = ["Research", "Cost", "Risk", "External"]
            for i, label in enumerate(parallel_labels):
                agent_cols[i].write(f"✅ {label}")
            
            # Collapsible Timeline
            with st.expander("▼ View Technical Execution Logs"):
                df = pd.DataFrame(meta["execution_df"])
                st.table(df[["agent", "duration"]])
                st.write(f"**Efficiency Metric:** {meta['speedup']:.2f}x speedup via LangGraph parallelism")

# Chat input
if prompt := st.chat_input("Ask a strategic question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        with st.status("🧠 Running Multi-Agent Workflow...") as status:
            try:
                # API Call
                response = requests.post(
                    f"{API_URL}/query",
                    json={"query": prompt, "user_id": user_id}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logs = data.get("execution_logs", [])
                    profile = data.get("user_profile", {})
                    
                    # Calculations
                    df = pd.DataFrame(logs)
                    total_seq = sum(df["duration"])
                    parallel_time = max(df["timestamp"] + df["duration"]) - min(df["timestamp"])
                    speedup = total_seq / parallel_time if parallel_time > 0 else 1.0
                    
                    # Confidence & Breakpoint
                    conf_val = data.get("confidence_score", 0.0)
                    # Check if summary_output already mentions a breakpoint or use 0.70 (Fix 2)
                    breakpoint_status = "Yes" if conf_val < 0.70 or "ANALYSIS HALTED" in data["result"] else "No"
                    
                    # Final content
                    final_ans = data["result"]
                    
                    # Metadata for storage
                    # Filter out Debate Agent from UI (Fix 7)
                    ui_logs = [log for log in logs if log["agent"] != "Debate Agent"]
                    df_ui = pd.DataFrame(ui_logs)

                    metadata = {
                        "profile_role": profile.get('role', 'User'),
                        "speedup": speedup,
                        "confidence": f"{int(conf_val*100)}%",
                        "breakpoint": breakpoint_status,
                        "execution_df": ui_logs,
                        "total_seq": total_seq,
                        "parallel_time": parallel_time
                    }
                    
                    status.update(label="✅ Analysis Complete", state="complete", expanded=False)
                    
                    # Display Answer
                    st.markdown(final_ans)
                    
                    # Display Analytics
                    st.divider()
                    cols = st.columns(4)
                    cols[0].metric("🧠 Profile Detected", metadata["profile_role"])
                    cols[1].metric("⚡ Parallel Gain", f"{metadata['speedup']:.1f}x")
                    cols[2].metric("🎯 Confidence", metadata["confidence"])
                    cols[3].metric("🛑 Breakpoint", metadata["breakpoint"])
                    
                    st.markdown("**Core Analysis Tracks:**")
                    agent_cols = st.columns(4)
                    parallel_labels = ["Research", "Cost", "Risk", "External"]
                    for i, label in enumerate(parallel_labels):
                        agent_cols[i].write(f"✅ {label}")
                        
                    with st.expander("▼ View Technical Execution Logs"):
                        st.table(df_ui[["agent", "duration"]])
                        st.write(f"**Efficiency Metric:** {speedup:.2f}x speedup via LangGraph parallelism")
                    
                    # Append response to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": final_ans,
                        "metadata": metadata
                    })
                    
                else:
                    status.update(label="❌ Analysis Failed", state="error")
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                status.update(label="❌ Connection Error", state="error")
                st.error(f"Failed to connect: {e}")
