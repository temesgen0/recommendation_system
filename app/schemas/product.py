# schemas/product.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    language: str  # Language of the product description

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
