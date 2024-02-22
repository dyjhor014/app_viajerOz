from pydantic import BaseModel
from datetime import datetime
from typing import List

class CategoryBase(BaseModel):
    id: int
    name: str
    description: str
    status: bool
    created_at: datetime

class CategoryList(BaseModel):
    categories: List[CategoryBase]
    
class CategoryCreate(BaseModel):
    name: str
    description: str
    
class CategoryUpdate(BaseModel):
    name: str = None
    description: str = None