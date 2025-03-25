import pytest

from config.settings import create_app
from instance.database import db as _db
from models.car import CarItem, CarRent
from shared import chrono


@pytest.fixture
def app():
    """Create a Flask application instance for testing."""
    app = create_app("config.testing")
    with app.app_context():
        _db.create_all()

    yield app  # di sini test nya jalan

    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def cars(app):
    cars = [
        {
            "brand": "TOYOTA",
            "license_plate": "B20AG",
            "frame_number": "222111",
            "model": "supra",
            "color": "red",
            "id": 1,
        },
        {
            "brand": "HONDA",
            "license_plate": "N2120FM",
            "frame_number": "2225555",
            "model": "jazz",
            "color": "blue",
            "id": 2,
        },
        {
            "brand": "SUZUKI",
            "license_plate": "AG7170LZ",
            "frame_number": "2223333",
            "model": "baleno",
            "color": "black",
            "id": 3,
        },
    ]
    with app.app_context():
        car_items = []
        for car in cars:
            car_item = CarItem(**car)
            car_items.append(car_item)
        print("POPULATING TEST DB")
        _db.session.add_all(car_items)
        _db.session.commit()
        print("INSERTED CAR TO TEST DB")
        return car_items


@pytest.fixture
def rented(app, cars):
    with app.app_context():
        car_rent = CarRent(
            car_id=1,
            customer_name="John Doe",
            customer_phone="123456789",
            rent_start=chrono.now(),
            rent_end=chrono.forward_days(3),
            hourly_rate=100,
        )
        _db.session.add(car_rent)
        _db.session.commit()
        return car_rent


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()
