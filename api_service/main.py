from fastapi import FastAPI, HTTPException, Body
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List
from datetime import datetime
import os
from models import Product, ProductCreate, Order, OrderCreate

app = FastAPI()

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "vegitrade_db")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    print(f"Connected to MongoDB at {MONGO_URL}")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Helper to fix _id
def fix_id(doc):
    doc["id"] = str(doc["_id"])
    return doc

@app.get("/")
async def root():
    return {"message": "Welcome to VegiTrade API"}

# --- Products ---
@app.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    product_dict["created_at"] = datetime.now()
    new_product = await app.mongodb["core_product"].insert_one(product_dict)
    created_product = await app.mongodb["core_product"].find_one({"_id": new_product.inserted_id})
    return fix_id(created_product)

@app.get("/products", response_model=List[Product])
async def list_products():
    products = []
    cursor = app.mongodb["core_product"].find()
    async for document in cursor:
        products.append(fix_id(document))
    return products

# --- Orders ---
@app.post("/orders", response_model=Order)
async def create_order(order: OrderCreate):
    # Verify product exists and has stock
    product = await app.mongodb["core_product"].find_one({"_id": ObjectId(order.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product["stock_kg"] < order.quantity_kg:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Calculate total price
    total_price = float(product["price_per_kg"]) * order.quantity_kg

    order_dict = order.dict()
    order_dict["total_price"] = total_price
    order_dict["created_at"] = datetime.now()
    
    # Update stock
    new_stock = product["stock_kg"] - order.quantity_kg
    await app.mongodb["core_product"].update_one(
        {"_id": ObjectId(order.product_id)},
        {"$set": {"stock_kg": new_stock}}
    )

    new_order = await app.mongodb["core_order"].insert_one(order_dict)
    created_order = await app.mongodb["core_order"].find_one({"_id": new_order.inserted_id})
    return fix_id(created_order)
