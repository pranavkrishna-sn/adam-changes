from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserProfile(BaseModel):
    id: int | None = None
    user_id: int
    full_name: str
    email: EmailStr
    phone_number: str | None = None
    address: str | None = None
    preferences: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)