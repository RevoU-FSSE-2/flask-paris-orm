from models.car import CarItem
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
