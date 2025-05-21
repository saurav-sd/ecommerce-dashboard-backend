from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.crud import category as crud_category
from app.db.session import get_db


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def Create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.
    """
    db_category = crud_category.create_category(db, category)
    return db_category

@router.get("/", response_model=list[CategoryOut])
def Get_all_categories(db: Session = Depends(get_db)):
    """
    Get all categories.
    """
    categories = crud_category.get_all_categories(db)
    return categories

@router.get("/{category_id}", response_model=CategoryOut)
def Get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """
    Get a category by ID.
    """
    category = crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryOut)
def update_category_by_id(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """
    Update a category by ID.
    """
    updated_category = crud_category.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category by ID.
    """
    deleted = crud_category.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")