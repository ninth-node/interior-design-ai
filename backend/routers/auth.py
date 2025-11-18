"""
Authentication endpoints for user registration and login
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from ..shared.database import get_db
from ..shared.models import User
from ..shared.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user_id,
)
from ..shared.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Request/Response Models
class UserRegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    role: Optional[str] = Field(default="designer", pattern="^(designer|admin|viewer)$")


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User information response"""
    user_id: str
    email: str
    full_name: Optional[str]
    role: str
    subscription_tier: str
    is_active: bool

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response with token and user info"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user

    - **email**: Valid email address (must be unique)
    - **password**: Password (min 8 characters)
    - **full_name**: User's full name
    - **role**: User role (designer, admin, or viewer) - defaults to designer

    Returns access token and user information
    """
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        user_id=uuid.uuid4(),
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        subscription_tier="starter",
        is_active=True
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(new_user.user_id),
            "email": new_user.email,
            "role": new_user.role,
            "is_active": new_user.is_active
        },
        expires_delta=access_token_expires
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            user_id=str(new_user.user_id),
            email=new_user.email,
            full_name=new_user.full_name,
            role=new_user.role,
            subscription_tier=new_user.subscription_tier,
            is_active=new_user.is_active
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login_user(
    credentials: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password

    - **email**: User's email address
    - **password**: User's password

    Returns access token and user information
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        },
        expires_delta=access_token_expires
    )

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            user_id=str(user.user_id),
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            subscription_tier=user.subscription_tier,
            is_active=user.is_active
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    result = await db.execute(
        select(User).where(User.user_id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        user_id=str(user.user_id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        subscription_tier=user.subscription_tier,
        is_active=user.is_active
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token

    Requires valid JWT token in Authorization header
    Returns a new access token
    """
    # Verify user still exists and is active
    result = await db.execute(
        select(User).where(User.user_id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        },
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
