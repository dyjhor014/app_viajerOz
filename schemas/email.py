from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    recipient_email: Optional[str] = None
    subject: str
    user_name: Optional[str] = None