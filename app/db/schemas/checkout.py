from pydantic import BaseModel
from typing import Optional

class CheckoutSchema(BaseModel):
    shipping_address: str
    billing_address: Optional[str] = None
    payment_method: str
