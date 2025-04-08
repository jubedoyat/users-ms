from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserBase, UserCreate, UserInDB, UserUpdate


def normalize_mongo_id(doc: dict) -> dict:
    """Convert MongoDB ObjectId to string for Pydantic compatibility."""
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["Users"]

    async def get_user_by_id(self, id: str) -> Optional[UserInDB]:
        if not ObjectId.is_valid(id):
            return None
        user = await self.collection.find_one({"_id": ObjectId(id)})
        return UserInDB(**normalize_mongo_id(user)) if user else None

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"email": email})
        return UserInDB(**normalize_mongo_id(user)) if user else None

    async def list_users(self) -> List[UserInDB]:
        users = []
        async for doc in self.collection.find():
            users.append(UserInDB(**normalize_mongo_id(doc)))
        return users

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        user_dict = user_data.model_dump()
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return UserInDB(**user_dict)

    async def update_user(self, id: str, update_data: UserUpdate) -> Optional[UserInDB]:
        if not ObjectId.is_valid(id):
            return None
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_dict}
        )
        user = await self.get_user_by_id(id)
        return user

    async def delete_user(self, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1
