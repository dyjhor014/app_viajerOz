from pydantic import BaseModel
from datetime import datetime
from typing import List

class LikeDislikePostBase(BaseModel):
    id: int
    post_id: int
    user_id: int
    action: str
    status: bool
    created_at: datetime

class LikeDislikePostList(BaseModel):
    like_dislike_posts: List[LikeDislikePostBase]

class LikeDislikePostCreate(BaseModel):
    post_id: int
    user_id: int
    action: str