from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from pydantic import BaseModel

app = FastAPI()

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for chat input
class ChatRequest(BaseModel):
    query: str

# Environment variables
REBRICKABLE_API_KEY = os.environ.get("REBRICKABLE_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
REBRICKABLE_BASE_URL = os.environ.get("REBRICKABLE_BASE_URL", "https://rebrickable.com/api/v3/lego/")

# Placeholder LLM response (replace with OpenAI or xAI API, see https://x.ai/api for xAI)
def get_llm_response(context, query):
    # Mock LLM response; integrate with OpenAI API or xAI API
    prompt = f"Based on this context: {context}, answer: {query}"
    # Example response (replace with actual API call)
    return {"response": f"Estimated price: ~${len(context) * 10} (based on context length)"}

# Fetch set data from Rebrickable
def fetch_set_data(set_num):
    if not REBRICKABLE_API_KEY:
        raise HTTPException(status_code=500, detail="Rebrickable API key not configured")
    
    url = f"{REBRICKABLE_BASE_URL}sets/{set_num}/"
    headers = {"Authorization": f"key {REBRICKABLE_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Set not found")
    return response.json()

# Root endpoint
@app.get("/")
async def read_root():
    return {"status": "OK", "message": "FastAPI backend is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "lego-price-rag-api",
        "api_status": {
            "rebrickable": "configured" if REBRICKABLE_API_KEY else "not_configured",
            "openai": "configured" if OPENAI_API_KEY else "not_configured"
        }
    }

# RAG endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    query = request.query.lower()
    if "price" in query or "cost" in query:
        # Extract set number (simplified parsing)
        set_num = query.split()[-1] if any(c.isdigit() for c in query) else "75192-1"
        try:
            set_data = fetch_set_data(set_num)
            context = f"Set: {set_data['name']}, Pieces: {set_data['num_parts']}, Year: {set_data['year']}"
            llm_response = get_llm_response(context, query)
            return {"response": llm_response["response"], "context": context}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"response": "Please ask about a LEGO set price (e.g., 'What's the price of 75192-1?')"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)