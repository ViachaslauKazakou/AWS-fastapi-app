from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    email: str

users_db = []

@router.post("/users/", response_model=User)
async def create_user(user: User):
    users_db.append(user)
    return user

@router.get("/users/", response_model=List[User])
async def get_users():
    return users_db