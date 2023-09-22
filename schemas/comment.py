from pydantic import BaseModel
from datetime import datetime
from typing import List

class CommentBase(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    like: int
    dislike: int
    status: bool
    created_at: datetime

class CommentList(BaseModel):
    comments: List[CommentBase]

class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    content: str
    like: int
    dislike: int