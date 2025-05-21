from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.db.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional

# Create a new product
def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Get a single product by ID
def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

# Get all products
def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).all()

# Update a product
def update_product(db: Session, product_id: int, updates: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


# Delete a product
def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True