from app.services.embedding import EmbeddingService
from app.utils.faiss_db import FAISSDB
from app.models.user import User
from app.models.product import Product
from app.models.interaction import Interaction
from app.services.database import SessionLocal
from app.schemas.product import ProductCreate
from app.schemas.user import UserCreate
from app.schemas.interaction import InteractionCreate

class RecommendationService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.faiss_db = FAISSDB()
        self.db = SessionLocal()

    def create_user(self, user: UserCreate):
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def add_product(self, product: ProductCreate):
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        # Generate embedding and store in FAISS
        embedding = self.embedding_service.generate_embedding(product.description)
        self.faiss_db.upsert_embedding(db_product.id, embedding)
        return db_product

    def log_interaction(self, interaction: InteractionCreate):
        db_interaction = Interaction(**interaction.dict())
        self.db.add(db_interaction)
        self.db.commit()
        self.db.refresh(db_interaction)
        return db_interaction

    def get_recommendations(self, user_id: int, top_k: int = 5):
        # Fetch user's interactions
        interactions = self.db.query(Interaction).filter(Interaction.user_id == user_id).all()
        if not interactions:
            return []
        # Get embeddings of interacted products
        product_ids = [interaction.product_id for interaction in interactions]
        products = self.db.query(Product).filter(Product.id.in_(product_ids)).all()
        embeddings = [self.embedding_service.generate_embedding(product.description) for product in products]
        # Average embeddings to represent user preferences
        user_embedding = sum(embeddings) / len(embeddings)
        # Query similar products
        results = self.faiss_db.query_similar(user_embedding, top_k)
        return results

    def find_related_products(self, product_id: int, top_k: int = 5,):
        """
        Find related products based on a product ID.
        """
        # Fetch the product by ID
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return []

        # Generate embedding for the product description
        embedding = self.embedding_service.generate_embedding(product.description)

        # Query FAISS for similar products
        results = self.faiss_db.query_similar(embedding, top_k)

        # Fetch product details from the database
        related_products = []
        for result in results:
            related_product = self.db.query(Product).filter(Product.id == result["product_id"]).first()
            if related_product:
                related_products.append(related_product)

        return related_products

    def search_products(self, query: str, top_k: int = 5):
        """
        Search products by a query string.
        """
        # Generate embedding for the search query
        embedding = self.embedding_service.generate_embedding(query)

        # Query FAISS for similar products
        results = self.faiss_db.query_similar(embedding, top_k)

        # Fetch product details from the database
        products = []
        for result in results:
            product = self.db.query(Product).filter(Product.id == result["product_id"]).first()
            if product:
                products.append(product)

        return products