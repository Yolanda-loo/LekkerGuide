from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Tour(Base):
    __tablename__ = "tours"

    # Use a UUID string for security (harder to guess than 1, 2, 3)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tourist_id = Column(String, nullable=False)
    guide_id = Column(String, nullable=False)
    
    # Status: pending, accepted, started, completed, cancelled
    status = Column(String, default="pending")
    
    # Location data
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    
    experience_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "experience": self.experience_type,
            "created_at": self.created_at.isoformat()
        }
