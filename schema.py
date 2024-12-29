"""
schema.py

This module contains the database models
"""

from sqlalchemy import Column, Integer, Float, String
from database import Base


class Product(Base):
    """This model represents the table in the database"""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    sku = Column(String(100))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String(100))
