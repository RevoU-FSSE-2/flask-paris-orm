from instance.database import db
from models.car import CarItem


def create_car_item(brand, license_plate, frame_number, model, color):
    """Create a car item."""
    car_item = CarItem(
        brand=brand,
        license_plate=license_plate,
        frame_number=frame_number,
        model=model,
        color=color,
    )
    db.session.add(car_item)
    db.session.commit()
    return car_item
