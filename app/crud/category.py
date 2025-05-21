from sqlalchemy.orm import Session
from app.db.models.category import Category
from app.db.schemas.category import CategoryCreate, CategoryUpdate



def create_category(db: Session, category: CategoryCreate):
    """
    Create a new category.
    """
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_all_categories(db: Session):
    """
    Get all categories.
    """
    return db.query(Category).all()


def get_category(db: Session, category_id: int):
    """
    Get a category by ID.
    """
    return db.query(Category).filter(Category.id == category_id).first()


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    """
    Update a category by ID.
    """
    db_category = get_category(db, category_id)
    if db_category:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        return db_category
    return None


def delete_category(db: Session, category_id: int):
    """
    Delete a category by ID.
    """
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False
