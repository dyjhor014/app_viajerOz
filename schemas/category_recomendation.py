from pydantic import BaseModel
from datetime import datetime
from typing import List

class CategoryRecomendationBase(BaseModel):
    id: int
    name: str
    description: str
    status: bool
    created_at: datetime
    
class CategoryRecomendationList(BaseModel):
    category_recomendations: List[CategoryRecomendationBase]

class CategoryRecomendationCreate(BaseModel):
    name:str
    description: str