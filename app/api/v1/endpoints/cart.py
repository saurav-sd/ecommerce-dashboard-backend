from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.cart import CartRead, CartCreate, CartUpdate
from app.db.session import get_db
from app.crud.cart import add_to_cart, get_cart_items, update_cart_item, remove_from_cart, clear_cart
from app.core.security import get_current_active_user
from app.db.models.user import User
from app.db.models.cart import Cart

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartRead])
def Get_cart_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all items in the user's cart.
    """
    return get_cart_items(db, current_user.id)

@router.post("/", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    cart_item: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add an item to the user's cart.
    """
    return add_to_cart(db, current_user.id, cart_item)

@router.put("/{cart_id}", response_model=CartRead)
def Update_cart_item(
    cart_id: int,
    cart_update: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an item in the user's cart.
    """
    cart_item = update_cart_item(db, cart_id, cart_update)
    if not cart_item or cart_item.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an item from the user's cart.
    """
    cart_item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == current_user.id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Item removed from cart"}

@router.delete("/")
def Clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Clear all items in the user's cart.
    """
    clear_cart(db, current_user.id)
    return {"detail": "Cart cleared successfully"}
