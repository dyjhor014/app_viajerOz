from pydantic import BaseModel
from datetime import datetime
from typing import List

class CityBase(BaseModel):
    id: int
    name: str
    description: str
    department_id: int
    status: bool
    created_at: datetime
    
class CityList(BaseModel):
    cities: List[CityBase]

class CityCreate(BaseModel):
    name: str
    description: str
    department_id: int