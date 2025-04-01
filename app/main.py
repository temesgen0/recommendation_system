from fastapi import FastAPI
from app.router.recommendation import router as reco_router

app = FastAPI()

app.include_router(reco_router)