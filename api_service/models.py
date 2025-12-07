from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price_per_kg: float
    stock_kg: float
    supplier_name: str
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_name: str
    product_id: str
    quantity_kg: float
    status: str = "PENDING"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True
