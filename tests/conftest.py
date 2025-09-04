import pytest
import asyncio
from httpx import AsyncClient
from tortoise import Tortoise
from app.main import app
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    test_db_url = "sqlite://:memory:"
    
    await Tortoise.init(
        db_url=test_db_url,
        modules={"models": ["models"]}
    )
    
    await Tortoise.generate_schemas()
    
    yield
    
    await Tortoise.close_connections()


@pytest.fixture
async def client(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user():
    """Test user data"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }

