from sqlalchemy.orm import Session
from app.db.models.order import Order, OrderItem
from app.db.schemas.order import OrderCreate, OrderItemCreate, OrderRead
from typing import List
from fastapi import HTTPException


def create_order(db: Session, order: OrderCreate, user_id: int) -> OrderRead:
    order_items = []
    total_amount = 0.0
    for item in order.items:
        db_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        order_items.append(db_item)
        total_amount += item.price * item.quantity
    db_order = Order(
        user_id=user_id,
        status="pending",
        total_amount=total_amount,
        items=order_items
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> OrderRead:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

def get_orders_by_user(db: Session, user_id: int) -> List[OrderRead]:
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

def update_order_status(db: Session, order_id: int, status: str) -> OrderRead:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order