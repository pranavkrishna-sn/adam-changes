from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class PasswordResetToken(BaseModel):
    id: int | None = None
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used: bool = False