from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from .venue import Venue

class EventBase(BaseModel):
    name: str
    date: datetime
    total_seats: int
    available_seats: int
    venue_id: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    venue: Venue

    class Config:
        orm_mode = True

    
