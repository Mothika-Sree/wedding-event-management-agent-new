from pydantic import BaseModel

class Vendor(BaseModel):
    id: int
    name: str
    vendor_type: str
    location: str
    price: float
    capacity: int
    rating: float
    available: bool