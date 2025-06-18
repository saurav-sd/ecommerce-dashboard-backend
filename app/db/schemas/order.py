from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float
    # Add any other fields you need for the order item

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

    class Config:
        orm_mode = True

class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: str

    class Config:
        orm_mode = True

class OrderCountResponse(BaseModel):
    count: int

    class Config:
        orm_mode = True