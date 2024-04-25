from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    id: int
    name: str
    dni: str
    email: str
    user: str
    password: str
    role: str
    group_id: Optional[int]
    routes: int
    status: bool
    created_at: datetime

class UserList(BaseModel):
    users: List[UserBase]

class UserCreate(BaseModel):
    name: str
    dni: Optional[str]
    email: str
    user: str
    password: str
    
class UserResponseToken(BaseModel):
    access_token: str
    token_type: str
    
class UserUpdate(BaseModel):
    name: str = None
    email: str = None
    user: str = None
    password: str = None
    group_id: int = None