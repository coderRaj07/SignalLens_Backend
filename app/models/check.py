from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.models import Base

class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"))
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=True)
    diff = Column(Text)
    summary = Column(Text)
    change_percentage = Column(Float, default=0.0)
    is_significant = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
