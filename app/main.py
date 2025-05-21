from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import product
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import category

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce Dashboard API!"}

@app.on_event("startup")
def startup_event():
    """
    Event handler for the startup event.
    Initializes the database.
    """
    init_db()
    print("Database initialized.")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(product.routes)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(category.router)