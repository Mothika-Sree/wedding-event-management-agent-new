from pydantic import BaseModel, Field
from datetime import date

class Event(BaseModel):
    event_type: str = Field(..., min_length=3)
    budget: float = Field(..., gt=0)
    location: str
    guest_count: int = Field(..., gt=0)
    event_date: date