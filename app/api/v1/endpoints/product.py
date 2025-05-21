from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas.product import ProductCreate, ProductUpdate, ProductOut
from typing import List
from app.db.models.product import Product
from app.crud.product import create_product, get_all_products, get_product, update_product, delete_product
import shutil
import uuid
import os


routes = APIRouter(prefix="/products", tags=["Products"])

@routes.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def Create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    db_product = create_product(db, product)
    return db_product


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
    

@routes.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = f"static/images/{file_name}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/images/{file_name}"
    return {"image_url": image_url}