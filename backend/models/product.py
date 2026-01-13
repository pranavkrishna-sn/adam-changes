from datetime import datetime
from pydantic import BaseModel, Field, PositiveFloat

class Product(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: PositiveFloat
    category_id: int
    stock: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True