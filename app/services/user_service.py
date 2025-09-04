from typing import Optional, List
from app.repositories.user_repo import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from datetime import timedelta


class UserService:
    """Service for user-related business logic"""

    @staticmethod
    async def create_user(user_data: UserCreate) -> Optional[UserResponse]:
        """Create a new user with hashed password"""
        # Check if user already exists
        if await UserRepository.user_exists(username=user_data.username):
            return None
        
        if await UserRepository.user_exists(email=user_data.email):
            return None
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = await UserRepository.create_user(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        
        if user:
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        return None

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[UserResponse]:
        """Authenticate user with username and password"""
        user = await UserRepository.get_user_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @staticmethod
    async def create_access_token_for_user(user: UserResponse, expires_delta: timedelta = None) -> str:
        """Create access token for authenticated user"""
        data = {"sub": user.username}
        return create_access_token(data=data, expires_delta=expires_delta)

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
        """Get user by ID"""
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        return None

    @staticmethod
    async def get_all_users(limit: int = 100, offset: int = 0) -> List[UserResponse]:
        """Get all users with pagination"""
        users = await UserRepository.get_all_users(limit=limit, offset=offset)
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """Update user information"""
        update_data = user_data.dict(exclude_unset=True)
        user = await UserRepository.update_user(user_id, **update_data)
        
        if user:
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        return None

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete user"""
        return await UserRepository.delete_user(user_id)
