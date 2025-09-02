from sqlalchemy.orm import Session
from app.db.models.order import Order, OrderItem
from app.db.schemas.order import OrderCreate, OrderItemCreate, OrderRead
from typing import List
from fastapi import HTTPException
from app.db.models.cart import Cart
from app.db.models.product import Product
from datetime import datetime
from app.db.schemas.checkout import CheckoutSchema



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

def create_order_from_cart(db: Session, user_id: int, data: CheckoutSchema):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        subtotal = product.price * item.quantity
        total_amount += subtotal
        order_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": product.price,
        })

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        payment_method=data.payment_method,
        shipping_address=data.shipping_address,
        billing_address=data.billing_address or data.shipping_address,
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(order_item)

    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    
    return order