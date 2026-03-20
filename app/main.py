from fastapi import FastAPI
from app.api.routes import router
from utils.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "intel agent platform is running"}