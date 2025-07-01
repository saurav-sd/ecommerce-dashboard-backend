from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.schemas.checkout import CheckoutSchema
from app.db.schemas.order import OrderOut
from app.db.models.order import Order, OrderItem
from app.db.models.cart import Cart
from app.db.models.product import Product
from app.db.session import get_db
from app.crud.order import create_order_from_cart
from app.core.security import get_current_active_user

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("/", response_model=OrderOut)
def checkout(
    order_data: CheckoutSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    order = create_order_from_cart(db, user_id=current_user.id, data=order_data)
    return order