from app.services.llm_service import llm_service

response = llm_service.call_model([
    {
        "role": "user",
        "content": "Reply with exactly: GitHub Models Connected"
    }
])

print(response)