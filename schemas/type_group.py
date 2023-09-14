from pydantic import BaseModel
from datetime import datetime
from typing import List

class TypeGroupBase(BaseModel):
    id: int
    name: str
    status: bool
    created_at: datetime  # Asegúrate de importar datetime desde datetime

class TypeGroupList(BaseModel):
    type_groups: List[TypeGroupBase]

class TypeGroupCreate(BaseModel):
    name: str

