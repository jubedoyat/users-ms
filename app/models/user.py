from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: str
    name: str
    age: int
    gender: str
    disability: str