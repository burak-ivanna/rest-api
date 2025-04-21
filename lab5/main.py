from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Library API with MongoDB"
)

app.include_router(router)
