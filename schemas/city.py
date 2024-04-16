from pydantic import BaseModel
from datetime import datetime
from typing import List
from .post import PostBase
from models.models import Post

class CityBase(BaseModel):
    id: int
    name: str
    description: str
    department_id: int
    status: bool
    created_at: datetime
    
class CityList(BaseModel):
    cities: List[CityBase]

class CityCreate(BaseModel):
    name: str
    description: str
    department_id: int
    
class CityUpdate(BaseModel):
    name: str = None
    description: str = None
    department_id: int = None
    
class CitiesPost(BaseModel):
    id: int
    name: str
    description: str
    department_id: int
    status: bool
    created_at: datetime
    posts: List[PostBase] = []
    
def map_post_to_postbase(post: Post) -> PostBase:
    return PostBase(
        id=post.id,
        title=post.title,
        date=post.date,
        brief=post.brief,
        content=post.content,
        user_id=post.user_id,
        category_id=post.category_id,
        city_origin=post.city_origin,
        city_destination=post.city_destination,
        like=post.like,
        dislike=post.dislike,
        comments=post.comments,
        status=post.status,
        created_at=post.created_at
    )