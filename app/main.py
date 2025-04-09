from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import users, auth
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.mongodb import get_database
from tests.test_users import get_test_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.dependency_overrides[get_database] = get_test_database
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
@app.get("/")
def root():
    return {"message": "Welcome to the Users Microservice!"}
app.include_router(auth.router)
app.include_router(users.router)