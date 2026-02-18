from pydantic import BaseModel
from datetime import datetime

class CheckOut(BaseModel):
    id: int
    diff: str | None
    summary: str | None
    change_percentage: float
    is_significant: bool
    created_at: datetime

    class Config:
        from_attributes = True
