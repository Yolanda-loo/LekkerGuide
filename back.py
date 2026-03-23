from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid

app = FastAPI(title="LekkerGuide API")

# --- DATA MODELS ---

class TourRequest(BaseModel):
    tourist_id: str
    guide_id: str
    experience_type: str  # e.g., "Food Adventure"
    lat: float
    lng: float

class TourResponse(BaseModel):
    tour_id: str
    status: str  # "pending", "accepted", "declined"
    timestamp: datetime

# --- MOCK DATABASE ---
# In a real app, this would be PostgreSQL or MongoDB
tours_db = {}

# --- ROUTES ---

@app.post("/request-tour", response_model=TourResponse)
async def create_tour_request(request: TourRequest):
    """
    This endpoint is hit when a Tourist clicks 'Book Instantly'
    """
    # 1. Generate a unique ID for this tour
    tour_id = str(uuid.uuid4())
    
    # 2. Create the tour object
    new_tour = {
        "tour_id": tour_id,
        "tourist_id": request.tourist_id,
        "guide_id": request.guide_id,
        "experience": request.experience_type,
        "location": {"lat": request.lat, "lng": request.lng},
        "status": "pending",
        "timestamp": datetime.now()
    }
    

    uvicorn.run(app, host="0.0.0.0", port=8000)
