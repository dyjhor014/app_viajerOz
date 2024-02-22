from pydantic import BaseModel
from datetime import datetime
from typing import List

class PostBase(BaseModel):
    id: int
    user_id: int
    category_id: int
    title: str
    date: str
    brief: str
    content: str
    city_origin: int
    city_destination: int
    like: int
    dislike: int
    status: bool
    created_at: datetime

class PostList(BaseModel):
    posts: List[PostBase]
    
class PostCreate(BaseModel):
    user_id: int
    category_id: int
    title: str
    date: str
    brief: str
    content: str
    city_origin: int
    city_destination: int
    like: int
    dislike: int
    
class PostUpdate(BaseModel):
    category_id: int
    title: str
    date: str
    brief: str
    content: str
    city_origin: int
    city_destination: int