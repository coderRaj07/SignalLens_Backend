from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models import Base

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    tag = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
