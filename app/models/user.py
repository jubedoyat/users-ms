from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str
    age: int
    email: EmailStr
    gender: str
    disability: str

class UserInDB(UserBase):
    id: str = Field(..., alias="_id")
    password: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    disability: Optional[str]
    password: Optional[str]

class UserPublic(UserBase):
    id: str = Field(..., alias="_id")