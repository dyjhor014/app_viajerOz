from pydantic import BaseModel
from datetime import datetime
from typing import List

class GroupBase(BaseModel):
    id: int
    type_id: int
    name: str
    status: bool
    created_at: datetime

class GroupList(BaseModel):
    groups: List[GroupBase]

class GroupCreate(BaseModel):
    type_id: int
    name: str