from pydantic import BaseModel


class PlanningRequest(BaseModel):
    request: str