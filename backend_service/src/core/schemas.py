"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """User registration schema."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema."""

    username: str
    password: str


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class QueryRequest(BaseModel):
    """Query request schema."""

    query: str = Field(..., min_length=1, max_length=2000)


class QueryResponse(BaseModel):
    """Query response schema."""

    response: str
    llm_model_used: str
    created_at: datetime


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str
    detail: Optional[str] = None
