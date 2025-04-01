import os
from sqlalchemy import Column, Integer, String
from app.services.database import Base
from sqlalchemy import create_engine

# models/product.py
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    language = Column(String)  # Language of the product description

# Database URL (PostgreSQL)
DATABASE_URL = "postgresql://postgres:1234@localhost:5433/recommendation_db"
# Read DATABASE_URL from environment variable
#DATABASE_URL = os.getenv("DATABASE_URL")
# Create the database engine
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)