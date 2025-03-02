from pydantic import BaseModel

class VenueBase(BaseModel):
    name: str
    location: str
    capacity: int

class VenueCreate(VenueBase):
    pass

class Venue(VenueBase):
    id: int
    
    class Config:
        orm_mode = True