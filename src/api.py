from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import logging

from db_utils import get_all_tournaments, get_tournaments_by_filter, get_tournament_stats
from data_collection import collect_tournaments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GenAI Sports Calendar API",
    description="API for managing sports tournament data using Hugging Face models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "GenAI Sports Calendar API",
        "version": "1.0.0",
        "endpoints": [
            "/tournaments",
            "/tournaments/filter",
            "/stats",
            "/refresh-data"
        ]
    }

@app.get("/tournaments")
async def get_tournaments(
    sport: Optional[str] = Query(None, description="Filter by sport"),
    level: Optional[str] = Query(None, description="Filter by level")
):
    try:
        if sport or level:
            tournaments = get_tournaments_by_filter(sport=sport, level=level)
        else:
            tournaments = get_all_tournaments()
        
        return {
            "success": True,
            "count": len(tournaments),
            "tournaments": tournaments
        }
        
    except Exception as e:
        logger.error(f"Error getting tournaments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tournaments/filter")
async def filter_tournaments(
    sport: Optional[str] = Query(None, description="Filter by sport"),
    level: Optional[str] = Query(None, description="Filter by level")
):
    try:
        tournaments = get_tournaments_by_filter(sport=sport, level=level)
        
        return {
            "success": True,
            "filters": {
                "sport": sport,
                "level": level
            },
            "count": len(tournaments),
            "tournaments": tournaments
        }
        
    except Exception as e:
        logger.error(f"Error filtering tournaments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        stats = get_tournament_stats()
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh-data")
async def refresh_data():
    try:
        tournaments = collect_tournaments()
        
        return {
            "success": True,
            "message": f"Data refreshed successfully. Collected {len(tournaments)} tournaments.",
            "count": len(tournaments)
        }
        
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
