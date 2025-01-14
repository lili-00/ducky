

### Service Layer


# filename: api/client/services/house_service.py

from typing import List
from ..models.house import House

class HouseService:
    def __init__(self):
        # This would ideally interface with a database
        self.houses: List[House] = []

    def add_house(self, house: House) -> None:
        self.houses.append(house)

    def list_houses(self) -> List[House]:
        return self.houses

    def find_house(self, house_id: int) -> House:
        for house in self.houses:
            if house.id == house_id:
                return house
        return None