from pydantic import BaseModel
from datetime import datetime
from typing import List

class LikeDislikeCommentBase(BaseModel):
    id: int
    comment_id: int
    user_id: int
    action: str
    status: bool
    created_at: datetime

class LikeDislikeCommentList(BaseModel):
    like_dislike_comments: List[LikeDislikeCommentBase]

class LikeDislikeCommentCreate(BaseModel):
    comment_id: int
    user_id: int
    action: str