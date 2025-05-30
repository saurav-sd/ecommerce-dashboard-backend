from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartBase(BaseModel):
    product_id: int
    quantity: int

class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    quantity: int

class CartRead(CartBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True