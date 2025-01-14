

### Core Layer - Domain Models


# filename: api/client/models/house.py

from pydantic import BaseModel

class House(BaseModel):
    id: int
    title: str
    description: str
    price_per_night: float
    location: str
    is_available: bool