from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import re
from pydantic import BaseModel
from typing import Optional, List
import openai

app = FastAPI()

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    query: str

class SetSearchRequest(BaseModel):
    query: str
    page_size: Optional[int] = 10

class SetInfo(BaseModel):
    set_num: str
    name: str
    year: int
    num_parts: int
    theme_id: Optional[int]
    theme_name: Optional[str]
    image_url: Optional[str]

# Environment variables
REBRICKABLE_API_KEY = os.environ.get("REBRICKABLE_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
REBRICKABLE_BASE_URL = os.environ.get("REBRICKABLE_BASE_URL", "https://rebrickable.com/api/v3/lego/")

# Initialize OpenAI client
if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(context, query, set_data=None):
    """Get intelligent price estimation from LLM"""
    if not OPENAI_API_KEY:
        # Fallback pricing logic when no LLM is available
        if set_data:
            pieces = set_data.get('num_parts', 0)
            year = set_data.get('year', 2020)
            
            # Basic price estimation based on pieces and age
            base_price_per_piece = 0.10  # $0.10 per piece base
            age_factor = max(1.0, (2024 - year) * 0.05)  # Older sets cost more
            estimated_price = pieces * base_price_per_piece * age_factor
            
            return {
                "response": f"Estimated retail price: ${estimated_price:.2f}\n"
                           f"(Based on {pieces} pieces and release year {year})\n"
                           f"Note: This is a basic estimation. Actual prices vary based on rarity, condition, and market demand."
            }
        return {"response": "Unable to estimate price without set data."}
    
    try:
        # Enhanced prompt for better price estimation
        prompt = f"""You are a LEGO price estimation expert. Based on this LEGO set information: {context}

Please provide a realistic price estimate considering:
- Number of pieces and complexity
- Release year (older/retired sets often cost more)
- Set popularity and rarity
- Current market trends

User query: {query}

Provide a helpful response with:
1. An estimated price range
2. Brief explanation of factors affecting the price
3. Note that prices vary by condition and market

Keep the response conversational and helpful."""

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful LEGO price estimation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return {"response": response.choices[0].message.content.strip()}
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback to basic estimation
        if set_data:
            pieces = set_data.get('num_parts', 0)
            estimated_price = pieces * 0.12  # Simple fallback
            return {
                "response": f"Estimated price: ${estimated_price:.2f} (basic estimation due to API unavailability)"
            }
        return {"response": "Unable to get price estimation at the moment."}

def extract_set_number(query):
    """Extract LEGO set number from query with improved regex"""
    # Common LEGO set number patterns
    patterns = [
        r'\b(\d{4,5}-\d+)\b',  # 75192-1, 10179-1 format
        r'\b(\d{4,5})\b',      # 75192, 10179 format
        r'set\s+(\d{4,5})',    # "set 75192"
        r'#(\d{4,5})',         # "#75192"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            set_num = match.group(1)
            # Add -1 if not present (most common variant)
            if '-' not in set_num:
                set_num += '-1'
            return set_num
    
    return None

def fetch_set_data(set_num):
    """Fetch set data from Rebrickable with better error handling"""
    if not REBRICKABLE_API_KEY:
        raise HTTPException(status_code=500, detail="Rebrickable API key not configured")
    
    url = f"{REBRICKABLE_BASE_URL}sets/{set_num}/"
    headers = {"Authorization": f"key {REBRICKABLE_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"LEGO set {set_num} not found")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Rebrickable API error")
        return response.json()
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="API request timeout")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

def search_sets_by_name(name, page_size=10):
    """Search for sets by name with enhanced functionality"""
    if not REBRICKABLE_API_KEY:
        return []
    
    url = f"{REBRICKABLE_BASE_URL}sets/"
    headers = {"Authorization": f"key {REBRICKABLE_API_KEY}"}
    params = {"search": name, "page_size": page_size}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

def get_set_parts(set_num):
    """Get parts list for a specific set"""
    if not REBRICKABLE_API_KEY:
        return []
    
    url = f"{REBRICKABLE_BASE_URL}sets/{set_num}/parts/"
    headers = {"Authorization": f"key {REBRICKABLE_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

def get_themes():
    """Get list of LEGO themes"""
    if not REBRICKABLE_API_KEY:
        return []
    
    url = f"{REBRICKABLE_BASE_URL}themes/"
    headers = {"Authorization": f"key {REBRICKABLE_API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

def get_sets_by_theme(theme_id, page_size=10):
    """Get sets by theme ID"""
    if not REBRICKABLE_API_KEY:
        return []
    
    url = f"{REBRICKABLE_BASE_URL}sets/"
    headers = {"Authorization": f"key {REBRICKABLE_API_KEY}"}
    params = {"theme_id": theme_id, "page_size": page_size}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
    except:
        pass
    return []

# Root endpoint
@app.get("/")
async def read_root():
    return {"status": "OK", "message": "FastAPI LEGO Price API is running"}

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

# API Endpoints for Rebrickable Integration

@app.get("/api/sets/{set_num}")
async def get_set(set_num: str):
    """Get specific LEGO set information"""
    try:
        set_data = fetch_set_data(set_num)
        return {
            "set_num": set_data['set_num'],
            "name": set_data['name'],
            "year": set_data['year'],
            "num_parts": set_data['num_parts'],
            "theme_id": set_data.get('theme_id'),
            "image_url": set_data.get('set_img_url'),
            "last_updated": set_data.get('last_modified_dt')
        }
    except HTTPException as e:
        raise e

@app.get("/api/sets/search")
async def search_sets(query: str, page_size: int = 10):
    """Search for LEGO sets by name"""
    sets = search_sets_by_name(query, page_size)
    return {
        "query": query,
        "results": sets,
        "count": len(sets)
    }

@app.get("/api/sets/{set_num}/parts")
async def get_set_parts_endpoint(set_num: str):
    """Get parts list for a specific set"""
    parts = get_set_parts(set_num)
    return {
        "set_num": set_num,
        "parts": parts,
        "count": len(parts)
    }

@app.get("/api/themes")
async def get_themes_endpoint():
    """Get all LEGO themes"""
    themes = get_themes()
    return {
        "themes": themes,
        "count": len(themes)
    }

@app.get("/api/themes/{theme_id}/sets")
async def get_sets_by_theme_endpoint(theme_id: int, page_size: int = 10):
    """Get sets by theme ID"""
    sets = get_sets_by_theme(theme_id, page_size)
    return {
        "theme_id": theme_id,
        "sets": sets,
        "count": len(sets)
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    return await process_chat_query(request.query)

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_input = data.get("query", "")
        return await process_chat_query(user_input)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")

async def process_chat_query(query: str):
    """Process chat query with improved logic"""
    if not query.strip():
        return {"response": "Please ask me about LEGO set prices!"}
    
    query_lower = query.lower()
    
    # Check if it's a price-related query
    price_keywords = ["price", "cost", "value", "worth", "expensive", "cheap", "retail"]
    is_price_query = any(keyword in query_lower for keyword in price_keywords)
    
    if is_price_query:
        # Try to extract set number
        set_num = extract_set_number(query)
        
        if set_num:
            try:
                set_data = fetch_set_data(set_num)
                context = (f"Set: {set_data['name']}, "
                          f"Pieces: {set_data['num_parts']}, "
                          f"Year: {set_data['year']}, "
                          f"Theme: {set_data.get('theme_id', 'N/A')}")
                
                llm_response = get_llm_response(context, query, set_data)
                return {
                    "response": llm_response["response"],
                    "context": context,
                    "set_info": {
                        "name": set_data['name'],
                        "set_num": set_data['set_num'],
                        "pieces": set_data['num_parts'],
                        "year": set_data['year']
                    }
                }
            except HTTPException as e:
                if e.status_code == 404:
                    return {"response": f"Sorry, I couldn't find LEGO set {set_num}. Please check the set number and try again."}
                else:
                    return {"response": f"Error fetching set data: {e.detail}"}
        else:
            # Try to search by name if no set number found
            search_terms = [word for word in query.split() if len(word) > 3 and word.lower() not in price_keywords]
            if search_terms:
                search_query = " ".join(search_terms)
                sets = search_sets_by_name(search_query)
                if sets:
                    suggestions = []
                    for s in sets[:3]:
                        suggestions.append(f"• {s['name']} ({s['set_num']})")
                    return {
                        "response": f"I found these LEGO sets matching '{search_query}':\n" + 
                                   "\n".join(suggestions) + 
                                   "\n\nPlease specify the set number for a price estimate."
                    }
            
            return {
                "response": "Please specify a LEGO set number (e.g., '75192') or include it in your question. "
                           "Example: 'What's the price of set 75192?' or 'How much does 10179-1 cost?'"
            }
    else:
        # Handle non-price queries
        return {
            "response": "I'm specialized in LEGO set price estimates! Ask me about the price or value of any LEGO set. "
                       "For example: 'What's the price of the Millennium Falcon 75192?' or 'How much does set 10179 cost?'"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)