from pydantic import BaseModel
from datetime import datetime
from typing import List

class LikeDislikeRecomendationBase(BaseModel):
    id: int
    recomendation_id: int
    user_id: int
    action: str
    status: bool
    created_at: datetime

class LikeDislikeRecomendationList(BaseModel):
    like_dislike_recomendations: List[LikeDislikeRecomendationBase]

class LikeDislikeRecomendationCreate(BaseModel):
    recomendation_id: int
    user_id: int
    action: str