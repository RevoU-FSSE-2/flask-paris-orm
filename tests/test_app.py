from models.car import CarItem
from models.users import User
from route.rent import RentItemRequest


def test_index(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200


def test_rent(client, rented):
    """Test the rent route."""
    response = client.get("/rent")
    print(response.json)
    assert response.status_code == 200


def test_create_rent(client, cars):
    """Test the rent route."""
    payload = RentItemRequest(
        car_id=1,
        customer_name="John Doe",
        customer_phone="123456789",
        days=2,
    )
    response = client.post("/rent", json=payload.model_dump())
    assert response.status_code == 201


def test_create_car_success(client, cars, db):
    """Test the create car route."""
    # brand
    # license_plate
    # frame_number
    # model
    # color
    response = client.post(
        "/car",
        json={
            "brand": "Toyota",
            "license_plate": "ABC123",
            "frame_number": "123456789",
            "model": "Corolla",
            "color": "White",
        },
    )
    assert response.status_code == 201
    assert response.json["success"]
    assert response.json["data"]["brand"] == "Toyota"
    query = db.select(CarItem).filter(CarItem.license_plate == "ABC123")
    data = db.session.execute(query).scalar_one()
    assert data.brand == "Toyota"
    assert data.license_plate == "ABC123"
    assert data.frame_number == "123456789"


def test_create_car_fail(client):
    """Test the create car route."""
    response = client.post(
        "/car",
        json={
            "license_plate": "ABC123",
            "frame_number": "123456789",
            "model": "Corolla",
            "color": "White",
        },
    )
    assert response.status_code == 400
    assert not response.json["success"]


def test_create_user_success(client, db):
    """Test successful user creation"""
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "securepassword123",
        },
    )

    assert response.status_code == 201
    assert response.json["success"]
    assert response.json["data"]["name"] == "Test User"
    assert response.json["data"]["email"] == "test@example.com"
    # Password should not be in response
    assert "password" not in response.json["data"]

    # Verify user was created in the database
    query = db.select(User).filter(User.email == "test@example.com")
    user = db.session.execute(query).scalar_one()
    assert user.name == "Test User"
    assert user.check_password("securepassword123")


def test_create_user_duplicate_email(client, db):
    """Test user creation with duplicate email"""
    # First create a user
    client.post(
        "/users",
        json={
            "name": "Original User",
            "email": "duplicate@example.com",
            "password": "password123456",
        },
    )

    # Try to create another user with the same email
    response = client.post(
        "/users",
        json={
            "name": "Duplicate User",
            "email": "duplicate@example.com",
            "password": "anotherpassword123",
        },
    )

    assert response.status_code == 400
    assert not response.json["success"]
    assert "already exists" in response.json["message"]


def test_create_user_invalid_data(client):
    """Test user creation with invalid data"""
    # Test with missing name
    response = client.post(
        "/users", json={"email": "missing@name.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert not response.json["success"]

    # Test with invalid email
    response = client.post(
        "/users",
        json={
            "name": "Invalid Email User",
            "email": "not-an-email",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert not response.json["success"]

    # Test with weak password
    response = client.post(
        "/users",
        json={
            "name": "Weak Password User",
            "email": "weak@password.com",
            "password": "short",  # Less than 8 characters
        },
    )
    assert response.status_code == 400
    assert not response.json["success"]


def test_login_session_success(client, db):
    """Test successful login with session authentication"""
    # First create a user
    client.post(
        "/users",
        json={
            "name": "Session User",
            "email": "session@example.com",
            "password": "sessionpassword123",
        },
    )
    
    # Login with session authentication
    response = client.post(
        "/users/login",
        json={
            "email": "session@example.com",
            "password": "sessionpassword123",
        },
    )
    
    assert response.status_code == 200
    assert response.json["success"]
    assert "data" in response.json
    assert "message" in response.json["data"]
    assert "Login successful" in response.json["data"]["message"]
    
    # Test accessing a protected route
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json["success"]
    assert response.json["data"]["email"] == "session@example.com"
    assert response.json["data"]["name"] == "Session User"


def test_login_jwt_success(client, db):
    """Test successful login with JWT authentication"""
    # First create a user
    client.post(
        "/users",
        json={
            "name": "JWT User",
            "email": "jwt@example.com",
            "password": "jwtpassword123",
        },
    )
    
    # Login with JWT authentication
    response = client.post(
        "/users/login?auth_type=jwt",
        json={
            "email": "jwt@example.com",
            "password": "jwtpassword123",
        },
    )
    
    assert response.status_code == 200
    assert response.json["success"]
    assert "data" in response.json
    assert "access_token" in response.json["data"]
    assert "refresh_token" in response.json["data"]
    
    # Get the token
    access_token = response.json["data"]["access_token"]
    
    # Test accessing a protected route with JWT
    response = client.get(
        "/users/me/jwt",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json["success"]
    assert response.json["data"]["email"] == "jwt@example.com"
    assert response.json["data"]["name"] == "JWT User"


def test_login_invalid_credentials(client, db):
    """Test login with invalid credentials"""
    # First create a user
    client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test_login@example.com",
            "password": "correctpassword123",
        },
    )
    
    # Try to login with wrong password
    response = client.post(
        "/users/login",
        json={
            "email": "test_login@example.com",
            "password": "wrongpassword123",
        },
    )
    
    assert response.status_code == 401
    assert not response.json["success"]
    
    # Try to login with non-existent email
    response = client.post(
        "/users/login",
        json={
            "email": "nonexistent@example.com",
            "password": "somepassword123",
        },
    )
    
    assert response.status_code == 401
    assert not response.json["success"]


def skiptest_jwt_token_refresh(client, db):
    """Test refreshing JWT token"""
    # First create a user
    client.post(
        "/users",
        json={
            "name": "Refresh User",
            "email": "refresh@example.com",
            "password": "refreshpassword123",
        },
    )
    
    # Login with JWT authentication
    response = client.post(
        "/users/login?auth_type=jwt",
        json={
            "email": "refresh@example.com",
            "password": "refreshpassword123",
        },
    )
    
    refresh_token = response.json["data"]["refresh_token"]
    
    # Use refresh token to get new access token
    response = client.post(
        "/users/token/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    
    assert response.status_code == 200
    assert response.json["success"]
    assert "data" in response.json
    assert "access_token" in response.json["data"]
    
    # Test the new access token
    new_access_token = response.json["data"]["access_token"]
    response = client.get(
        "/users/me/jwt",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    
    assert response.status_code == 200
    assert response.json["success"]
    assert response.json["data"]["email"] == "refresh@example.com"


def test_logout(client, db):
    """Test user logout for session authentication"""
    # First create a user
    client.post(
        "/users",
        json={
            "name": "Logout User",
            "email": "logout@example.com",
            "password": "logoutpassword123",
        },
    )
    
    # Login with session authentication
    client.post(
        "/users/login",
        json={
            "email": "logout@example.com",
            "password": "logoutpassword123",
        },
    )
    
    # Verify login was successful by accessing protected route
    response = client.get("/users/me")
    assert response.status_code == 200
    
    # Logout
    response = client.post("/users/logout")
    assert response.status_code == 200
    assert response.json["success"]
    
    # Verify logout was successful by trying to access protected route
    response = client.get("/users/me")
    assert response.status_code != 200  # Should be redirected or access denied
