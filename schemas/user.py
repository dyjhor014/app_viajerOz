from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    id: int
    name: str
    email: str
    user: str
    password: str
    rol: int
    group_id: int
    routes: int
    status: bool
    created_at: datetime

class UserList(BaseModel):
    users: List[UserBase]

class UserCreate(BaseModel):
    name: str
    email: str
    user: str
    password: str
    rol: int
    group_id: int
    routes: int
    
class UserResponseToken(BaseModel):
    access_token: str
    token_type: str