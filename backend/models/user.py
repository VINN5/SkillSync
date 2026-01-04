from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from bson import ObjectId
import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Literal["client", "contractor"]

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    is_active: bool = True

class UserResponse(UserBase):
    id: str
    created_at: datetime.datetime

    class Config:
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat(),
        }