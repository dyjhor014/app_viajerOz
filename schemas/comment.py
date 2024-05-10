from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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
    post_id: Optional[int] = None
    user_id: Optional[int] = None
    content: str
    
class CommentUpdate(BaseModel):
    content: str
    
class CommentResponse(BaseModel):
    post_id: int
    user_id: int
    content: str
    created_at: datetime