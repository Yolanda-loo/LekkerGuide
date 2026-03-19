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
    
    # 3. Save to database
    tours_db[tour_id] = new_tour
    
    # 4. LOGIC: Trigger a notification to the Guide
    # In a real app, you would use WebSockets (Socket.io) here 
    # to 'push' the request to the Guide's dashboard instantly.
    print(f"ALERTER: Notifying Guide {request.guide_id} of a new request!")

    return TourResponse(
        tour_id=tour_id, 
        status="pending", 
        timestamp=new_tour["timestamp"]
    )

@app.patch("/update-tour-status/{tour_id}")
async def update_status(tour_id: str, status: str):
    """
    This endpoint is hit when a Guide clicks 'ACCEPT' or 'DECLINE'
    """
    if tour_id not in tours_db:
        raise HTTPException(status_code=404, detail="Tour not found")
    
    tours_db[tour_id]["status"] = status
    return {"message": f"Tour {status}", "tour_id": tour_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
