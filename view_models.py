"""
view_models.py

This module contians the design for request and response models
"""

from pydantic import BaseModel, Field


class ProductRequestModel(BaseModel):
    """
    This model represents the request for Product
    """

    name: str = Field(title="name of the product")
    sku: str = Field(title="sku of the product")
    price: float = Field(gt=0,description="Price should be greater than 0")
    stock: int = Field(ge=0,description="Stock should be greater than 0")
    description: str = Field(title="description of the product")


class ProductResponseModel(BaseModel):
    """
    This model represents the request for Product
    """

    id: int
    name: str
    sku: str
    price: float
    stock: int
    description: str
    
    class Config:
        orm_mode = True
