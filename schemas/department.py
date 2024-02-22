from pydantic import BaseModel
from datetime import datetime
from typing import List

class DepartmentBase(BaseModel):
    id: int
    name: str
    description: str
    status: bool
    created_at: datetime
    
class DepartmentList(BaseModel):
    departments: List[DepartmentBase]

class DepartmentCreate(BaseModel):
    name: str
    description: str

class DepartmentUpdate(BaseModel):
    name: str = None
    description: str = None