from pydantic import BaseModel
from datetime import datetime
from typing import List

class TypeVehicleBase(BaseModel):
    id: int
    name: str
    status: bool
    created_at: datetime

class TypeVehicleList(BaseModel):
    type_vehicles: List[TypeVehicleBase]

class TypeVehicleCreate(BaseModel):
    name: str

