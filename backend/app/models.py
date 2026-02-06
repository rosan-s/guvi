from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from .db import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    industry = Column(String, nullable=False)
    revenue = Column(Float, nullable=True)
    expenses = Column(Float, nullable=True)
    net_margin = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    creditworthiness = Column(String, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
