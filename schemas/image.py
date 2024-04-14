from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ImageBase(BaseModel):
    id: int
    post_id: int
    user_id: int
    name: str
    description: str
    url: str
    status: bool
    created_at: datetime
    
class ImageList(BaseModel):
    images: List[ImageBase]

class ImageCreate(BaseModel):
    post_id: int
    user_id: Optional[int] = None
    name: str
    description: str
    url: str

class ImageUpdate(BaseModel):
    name: str
    description: str
    url: str