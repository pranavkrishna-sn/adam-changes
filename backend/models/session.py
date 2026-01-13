from datetime import datetime
from pydantic import BaseModel, Field

class Session(BaseModel):
    id: int | None = None
    user_id: int
    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True