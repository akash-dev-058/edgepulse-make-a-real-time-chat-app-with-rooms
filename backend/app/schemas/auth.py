from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    type: str


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)



class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class RefreshToken(BaseModel):
    refresh_token: str
