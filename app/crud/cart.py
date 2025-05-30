from sqlalchemy.orm import Session
from app.db.schemas.cart import CartCreate, CartUpdate, CartRead
from app.db.models.cart import Cart
from typing import List, Optional


def get_cart_item(db: Session, user_id: int, product_id: int) -> Optional[Cart]:
    """
    Get a specific cart item by user ID and product ID.
    """
    return db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()

def get_cart_items(db: Session, user_id: int) -> List[Cart]:
    """
    Get all cart items for a specific user.
    """
    return db.query(Cart).filter(Cart.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, cart_item: CartCreate) -> Cart:
    db_cart = get_cart_item(db, user_id, cart_item.product_id)
    if db_cart:
        # If the item already exists in the cart, update the quantity
        db_cart.quantity += cart_item.quantity
        db.add(db_cart)
    else:
        # Create a new cart item
        db_cart = Cart(user_id=user_id, **cart_item.dict())
        db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def update_cart_item(db: Session, cart_id: int, cart_update: CartUpdate) -> Optional[Cart]:
    """
    Update a specific cart item.
    """
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if db_cart:
        db_cart.quantity = cart_update.quantity
        db.commit()
        db.refresh(db_cart)
    return db_cart

def remove_from_cart(db: Session, cart_id: int) -> None:
    """
    Remove a specific cart item.
    """
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
    else:
        raise ValueError("Cart item not found")
    
def clear_cart(db: Session, user_id: int) -> None:
    """
    Clear all cart items for a specific user.
    """
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()