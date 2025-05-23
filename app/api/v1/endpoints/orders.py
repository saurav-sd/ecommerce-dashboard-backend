from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.schemas.order import OrderCreate, OrderRead
from app.db.models.order import Order
from app.db.session import get_db
from app.crud.order import create_order, get_order, update_order_status
from app.api.v1.endpoints import auth
from typing import List
from app.core.security import get_current_active_user


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/orders/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_active_user)
):
    """
    Create a new order.
    """
    return create_order(db=db, order=order, user_id=current_user.id)


@router.get("/orders/{order_id}", response_model=OrderRead)
async def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_active_user)
):
    """
    Get an order by ID.
    """
    order = get_order(db=db, order_id=order_id)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this order")
    return order


@router.patch("/{order_id}/status", response_model=OrderRead)
async def Update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: auth.User = Depends(get_current_active_user)
):
    """
    Update the status of an order.
    """
    order = get_order(db=db, order_id=order_id)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this order")
    return update_order_status(db=db, order_id=order_id, status=status)