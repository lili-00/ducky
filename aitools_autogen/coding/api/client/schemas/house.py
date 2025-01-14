

### Schemas


# filename: api/client/schemas/house.py

from pydantic import BaseModel

class HouseBase(BaseModel):
    title: str
    description: str
    price_per_night: float
    location: str

class HouseCreate(HouseBase):
    pass

class HouseDisplay(HouseBase):
    id: int
    is_available: bool