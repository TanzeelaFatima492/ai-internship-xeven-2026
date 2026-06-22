from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic Model
class Item(BaseModel):
    name: str
    price: float


# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}


# Health Check Endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}


# Path Parameter Example
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "message": "Item retrieved successfully"
    }


# POST Endpoint
@app.post("/items")
def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }