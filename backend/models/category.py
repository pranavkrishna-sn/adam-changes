from datetime import datetime
from pydantic import BaseModel, Field

class Category(BaseModel):
    id: int | None = None
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)