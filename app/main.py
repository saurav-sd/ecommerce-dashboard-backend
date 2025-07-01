from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import product
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import category
from app.api.v1.endpoints import orders
from app.api.v1.endpoints import cart
from app.api.v1.endpoints import checkout
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(orders.router)

app.include_router(cart.router)

app.include_router(checkout.router)


origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Add allowed origins here
    allow_credentials=True,             # Needed for cookies/auth
    allow_methods=["*"],                # Allow all HTTP methods
    allow_headers=["*"],                # Allow all headers
)