from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base schema shared across create and update
class ProductBase(BaseModel):
    title: str = Field(..., example="Wireless Mouse")
    description: Optional[str] = Field(None, example="Ergonomic wireless mouse with 2.4GHz connection")
    price: float = Field(..., example=19.99)
    stock: int = Field(0, example=100)
    category: Optional[str] = Field(None, example="Electronics")
    image: Optional[str] = Field(None, example="https://example.com/image.jpg")

# Schema for creating a product
class ProductCreate(ProductBase):
    pass

# Schema for updating a product (all fields optional)
class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category: Optional[str]
    image: Optional[str]

# Schema for returning a product in responses
class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True