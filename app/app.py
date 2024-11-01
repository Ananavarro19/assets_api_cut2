from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Asset Management System")

app.include_router(router, prefix="/api")