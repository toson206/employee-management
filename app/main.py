from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.departments import router as departments_router
from app.routers.employees import router as employees_router
from app.routers.users import router as users_router


app = FastAPI(
    title="Employee Management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(departments_router)
app.include_router(employees_router)
app.include_router(users_router)


@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to Employee Management API",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "Employee Management API",
        "version": "1.0.0"
    }





@app.get("/api/test")
def test_api():
    return {"message": "Test push code"}

