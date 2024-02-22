from pydantic import BaseModel
from datetime import datetime
from typing import List

class VehicleBase(BaseModel):
    id: int
    user_id: int
    type_vehicle_id: int
    brand: str
    model: str
    year: str
    registration : str
    image: str
    status: bool
    created_at: datetime

class VehicleList(BaseModel):
    vehicles: List[VehicleBase]

class VehicleCreate(BaseModel):
    user_id: int
    type_vehicle_id: int
    brand: str
    model: str
    year: str
    registration : str
    image: str
    
class VehicleUpdate(BaseModel):
    brand: str = None
    model: str = None
    year: str = None
    registration: str = None
    image: str = None
    