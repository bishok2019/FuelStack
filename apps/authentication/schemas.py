from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserList(UserBase):
    id: int

    # password: str
    model_config = ConfigDict(from_attributes=True)


class UserRetrieve(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    username: str
    password: str


class LogoutRequest(BaseModel):
    refresh_token: str
