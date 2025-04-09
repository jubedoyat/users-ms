import pytest
from httpx import AsyncClient
from app.main import app
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "name": "Test User",
            "age": 25,
            "gender": "male",
            "email": "test@example.com",
            "password": "securepass",
            "disability": "None"
        })
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"

async def get_test_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["test_db"]
    yield db

