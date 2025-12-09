# backend/data/models.py
from sqlalchemy import Column, Integer, String
from .base import Base

class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key = True)
    text = Column(String(255), nullable=False, unique=True)