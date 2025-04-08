from fastapi import APIRouter, HTTPException, Depends, status, Path
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.models.user import UserCreate, UserUpdate, UserPublic, UserInDB
from app.core.security import hash_password
from app.db.mongodb import get_database
from app.db.repositories.user_repo import UserRepository
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = hash_password(user.password)
    new_user = await user_repo.create_user(user)
    return UserPublic(**new_user.model_dump())

@router.patch("/{id}", response_model=UserPublic)
async def update_user(
    id: str = Path(..., description="User MongoDB ID"),
    user_update: UserUpdate = ...,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_repo = UserRepository(db)

    if user_update.password:
        user_update.password = hash_password(user_update.password)

    updated_user = await user_repo.update_user(id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserPublic(**updated_user.model_dump())

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str = Path(..., description="User MongoDB ID"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_repo = UserRepository(db)
    deleted = await user_repo.delete_user(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return
