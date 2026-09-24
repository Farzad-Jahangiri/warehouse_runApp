from pydantic import BaseModel
from typing import Optional

class IntroCodePost(BaseModel):
    phone: str
    error: Optional[str] = None
    message: Optional[str] = None