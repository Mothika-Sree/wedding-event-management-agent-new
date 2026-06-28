from typing import TypedDict, Optional

class EventState(TypedDict):
    messages: list

    event_type: Optional[str]
    city: Optional[str]
    guests: Optional[int]
    budget: Optional[int]
    date: Optional[str]

    current_step: Optional[str]

    venue: Optional[dict]
    catering: Optional[dict]
    decorator: Optional[dict]
    photographer: Optional[dict]