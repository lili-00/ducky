

### Data Layer

# For simplicity, the service layer is acting as our data layer by interfacing directly with a list of houses. In a real-world scenario, this layer would interact with a database.

### Web Layer - API Endpoints


# filename: api/client/main.py

from fastapi import FastAPI, HTTPException
from .schemas.house import HouseCreate, HouseDisplay
from .services.house_service import HouseService
from .models.house import House

app = FastAPI()
house_service = HouseService()

@app.post("/houses/", response_model=HouseDisplay)
def create_house(house: HouseCreate):
    new_house = House(**house.dict(), id=len(house_service.houses) + 1, is_available=True)
    house_service.add_house(new_house)
    return new_house

@app.get("/houses/", response_model=list[HouseDisplay])
def list_houses():
    return house_service.list_houses()

@app.get("/houses/{house_id}", response_model=HouseDisplay)
def get_house(house_id: int):
    house = house_service.find_house(house_id)
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return house