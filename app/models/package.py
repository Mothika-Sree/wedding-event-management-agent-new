from pydantic import BaseModel


class EventPackage(BaseModel):
    package_id: int
    venue: str
    caterer: str
    decorator: str
    photographer: str
    total_cost: float
    overall_score: float
    package_score: float