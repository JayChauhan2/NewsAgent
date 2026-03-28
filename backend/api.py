from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

# Add project root to sys.path to allow imports from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Enable CORS for React frontend (allow all in development/deployment for simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to data files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, 'public', 'articles.json')
ASSIGNMENTS_FILE = os.path.join(BASE_DIR, 'public', 'assignments.json')

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

from fastapi.responses import JSONResponse

@app.get("/")
def read_root():
    return {"status": "The Printing Press is running"}

@app.get("/articles")
def get_articles():
    content = load_json(ARTICLES_FILE)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate", 
        "Pragma": "no-cache", 
        "Expires": "0"
    }
    return JSONResponse(content=content, headers=headers)

@app.get("/assignments")
def get_assignments():
    content = load_json(ASSIGNMENTS_FILE)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate", 
        "Pragma": "no-cache", 
        "Expires": "0"
    }
    return JSONResponse(content=content, headers=headers)

@app.get("/agent_status.json")
def get_agent_status():
    status_file = os.path.join(BASE_DIR, 'public', 'agent_status.json')
    content = load_json(status_file)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate", 
        "Pragma": "no-cache", 
        "Expires": "0"
    }
    return JSONResponse(content=content, headers=headers)

from fastapi import HTTPException, Header
from backend import run_news_cycle
from backend.writer import publisher

@app.get("/trigger-publish")
def trigger_publish(x_cron_secret: str = Header(None)):
    """
    Endpoint for Vercel Cron to trigger the publisher loop.
    """
    secret = os.getenv("CRON_SECRET")
    if secret and x_cron_secret != secret:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    try:
        publisher.publish_pending_dossiers()
        return {"status": "success", "message": "Publisher run completed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/trigger-cycle")
def trigger_cycle(x_cron_secret: str = Header(None)):
    """
    Endpoint for Vercel Cron to trigger the news cycle.
    """
    secret = os.getenv("CRON_SECRET")
    if secret and x_cron_secret != secret:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    try:
        run_news_cycle.run_cycle()
        return {"status": "success", "message": "News cycle completed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/articles/{article_id}")
def delete_article(article_id: str):
    articles = load_json(ARTICLES_FILE)
    
    # Filter out the article
    new_articles = [a for a in articles if a.get('id') != article_id]
    
    if len(new_articles) < len(articles):
        with open(ARTICLES_FILE, 'w') as f:
            json.dump(new_articles, f, indent=2)
        return {"status": "success", "message": f"Article {article_id} deleted"}
    
    return {"status": "error", "message": "Article not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
