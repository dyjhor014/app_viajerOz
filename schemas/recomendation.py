from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class RecomendationBase(BaseModel):
    id: int
    category_recomendation_id: int
    post_id: int
    user_id: int 
    city_id: int 
    name: str
    detail: str
    location: str 
    like: int
    dislike: int
    status: bool
    created_at: datetime

class RecomendationList(BaseModel):
    recomendations: List[RecomendationBase]

class RecomendationCreate(BaseModel):
    category_recomendation_id: int
    post_id: int
    user_id: Optional[int] = None 
    city_id: int 
    name: str
    detail: str
    location: str
    
class RecomendationUpdate(BaseModel):
    name: str
    detail: str
    location: str 
    like: int
    dislike: int