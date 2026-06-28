from datetime import date

from app.models.event import Event
from app.services.event_service import EventService


event = Event(
    event_type="Wedding",
    budget=500000,
    location="Chennai",
    guest_count=300,
    event_date=date(2027, 1, 15)
)

EventService.create_event(event)

print(
    EventService.get_event()
)