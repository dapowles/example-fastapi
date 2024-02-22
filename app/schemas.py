from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
import email_validator

## USERS ##
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    created_at: datetime

    class Config:
        from_attributes = True

## AUTH ##
class UserCredentials(BaseModel):
    email: EmailStr
    password: str

## POSTS ##
class PostBase(BaseModel):
    title: str
    content: str
    
    
class PostCreate(PostBase):
    published: bool = True

class PostResponse(PostBase):
    published_date: datetime
    id: int
    user_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


