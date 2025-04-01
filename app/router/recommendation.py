from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.recommendation import RecommendationService
from app.schemas.product import ProductCreate, ProductResponse
from app.schemas.user import UserCreate
from app.schemas.interaction import InteractionCreate
from app.services.database import get_db

router = APIRouter()

# Initialize services
recommendation_service = RecommendationService()
@router.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return recommendation_service.create_user(user)

@router.post("/products/")
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return recommendation_service.add_product(product)

@router.post("/interactions/")
async def log_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    return recommendation_service.log_interaction(interaction)

@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, top_k: int = 5, db: Session = Depends(get_db)):
    return recommendation_service.get_recommendations(user_id, top_k)


@router.get("/products/{product_id}/related", response_model=list[ProductResponse])
async def get_related_products(product_id: int, top_k: int = 5):
    """
    Get related products for a given product ID.
    """
    return recommendation_service.find_related_products(product_id, top_k)

@router.get("/products/search", response_model=list[ProductResponse])
async def search_products(query: str, top_k: int = 5):
    """
    Search products by a query string.
    """
    return recommendation_service.search_products(query, top_k)