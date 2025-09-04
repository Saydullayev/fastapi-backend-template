from typing import Optional, List
from tortoise.exceptions import DoesNotExist
from app.models.user import User


class UserRepository:
    @staticmethod
    async def create_user(username: str, email: str, hashed_password: str, full_name: str = None) -> User:
        """Create a new user"""
        user = await User.create(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        return user

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        try:
            return await User.get(username=username)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return await User.get(email=email)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all_users(limit: int = 100, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        return await User.all().limit(limit).offset(offset)

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> Optional[User]:
        """Update user information"""
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            await user.update_from_dict(kwargs)
            await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete user"""
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            await user.delete()
            return True
        return False

    @staticmethod
    async def user_exists(username: str = None, email: str = None) -> bool:
        """Check if user exists by username or email"""
        if username:
            return await User.filter(username=username).exists()
        if email:
            return await User.filter(email=email).exists()
        return False
