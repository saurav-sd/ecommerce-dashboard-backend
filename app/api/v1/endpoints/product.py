from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas.product import ProductCreate, ProductUpdate, ProductOut
from typing import List
from app.db.models.product import Product
from app.db.models.category import Category
from app.crud.product import create_product, get_all_products, get_product, update_product, delete_product
import shutil
import uuid
import os
from sqlalchemy.exc import IntegrityError
from app.cloudinary_config import cloudinary


routes = APIRouter(prefix="/products", tags=["Products"])

@routes.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def Create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    # try:
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    db_product = create_product(db, product)
    return db_product
    # except IntegrityError as e:
    #     db.rollback()
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Invalid category_id or related foreign key does not exist."
    #     )


@routes.get("/", response_model=List[ProductOut])
def Get_all_products(db: Session = Depends(get_db)):
    """
    Get all products.
    """
    products = get_all_products(db)
    return products

@routes.get("/{product_id}", response_model=ProductOut)
def Get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Get a product by ID.
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@routes.put("/{product_id}", response_model=ProductOut)
def update_product_by_id(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update a product by ID.
    """
    updated_product = update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product


@routes.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by ID.
    """
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": f"Product with ID {product_id} has been deleted successfully."}

@routes.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(file.file, folder="ecommerce_uploads")

        return {
            "image_url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")