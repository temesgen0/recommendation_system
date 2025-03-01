import os
from sqlalchemy import Column, Integer, String
from app.services.database import Base
from sqlalchemy import create_engine

# models/interaction.py
class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    interaction_type = Column(String)  # e.g., "click", "purchase"

# Database URL (PostgreSQL)
#DATABASE_URL = "postgresql://postgres:1234@localhost:5433/recommendation_db"

# Read DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)