from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Policy Search Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    text: str

def search_local_policy(query: str) -> str:
    file_path = "data/policy_docs.txt"
    if not os.path.exists(file_path):
        return "No specific local policy clauses found matching your query keywords."
        
    with open(file_path, "r") as f:
        content = f.read()
        
    sections = content.split("[SECTION:")
    matched_context = []
    words = query.lower().split()
    
    for section in sections:
        if not section.strip():
            continue
        if any(word in section.lower() for word in words):
            matched_context.append(f"[SECTION: {section.strip()}")
            
    if not matched_context:
        return "No specific local policy clauses found matching your query keywords."
        
    return "\n\n".join(matched_context)

@app.post("/api/query")
async def handle_query(request: QueryRequest):
    clean_query = request.text.strip()
    if not clean_query:
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")
        
    relevant_context = search_local_policy(clean_query)
    mock_ai_synthesis = f"Based on the analysed guidelines, here is the relevant context: \n\n{relevant_context}"
    
    return {
        "query": clean_query,
        "answer": mock_ai_synthesis,
        "sources_found": len(relevant_context.split("[SECTION:")) - 1 if "SECTION" in relevant_context else 0
    }
