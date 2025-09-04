import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, test_user: dict):
    """Test user registration"""
    response = await client.post("/api/v1/users/register", json=test_user)
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_user(client: AsyncClient, test_user: dict):
    """Test duplicate user registration"""
    # First registration
    await client.post("/api/v1/users/register", json=test_user)
    
    # Second registration with same username
    response = await client.post("/api/v1/users/register", json=test_user)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, test_user: dict):
    """Test user login"""
    # First register the user
    await client.post("/api/v1/users/register", json=test_user)
    
    # Then try to login
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = await client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user: dict):
    """Test login with invalid credentials"""
    # First register the user
    await client.post("/api/v1/users/register", json=test_user)
    
    # Try to login with wrong password
    login_data = {
        "username": test_user["username"],
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_current_user_info(client: AsyncClient, test_user: dict):
    """Test getting current user info"""
    # Register and login
    await client.post("/api/v1/users/register", json=test_user)
    login_response = await client.post("/api/v1/users/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Get current user info
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, test_user: dict):
    """Test getting user by ID"""
    # Register and login
    await client.post("/api/v1/users/register", json=test_user)
    login_response = await client.post("/api/v1/users/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user info to get the ID
    me_response = await client.get("/api/v1/users/me", headers=headers)
    user_id = me_response.json()["id"]
    
    # Get user by ID
    response = await client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == test_user["username"]


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, test_user: dict):
    """Test updating user information"""
    # Register and login
    await client.post("/api/v1/users/register", json=test_user)
    login_response = await client.post("/api/v1/users/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user info to get the ID
    me_response = await client.get("/api/v1/users/me", headers=headers)
    user_id = me_response.json()["id"]
    
    # Update user
    update_data = {"full_name": "Updated Test User"}
    response = await client.put(f"/api/v1/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["full_name"] == "Updated Test User"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test unauthorized access to protected endpoints"""
    # Try to access protected endpoint without token
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
