from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.services.recommendation import RecommendationService
from app.schemas.product import ProductCreate
from app.schemas.user import UserCreate
from app.schemas.interaction import InteractionCreate
from app.services.database import get_db

app = FastAPI()

# Initialize services
recommendation_service = RecommendationService()

@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return recommendation_service.create_user(user)

@app.post("/products/")
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return recommendation_service.add_product(product)

@app.post("/interactions/")
async def log_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    return recommendation_service.log_interaction(interaction)

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    return recommendation_service.get_recommendations(user_id, top_k)