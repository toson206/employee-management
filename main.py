from fastapi import FastAPI
from app.routers.employees import router

app = FastAPI(
    title="Employee Management API",
    version="1.0.0"
)

app.include_router(router)