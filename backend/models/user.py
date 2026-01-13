from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int | None = None
    email: EmailStr
    password_hash: str = Field(..., min_length=60)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True