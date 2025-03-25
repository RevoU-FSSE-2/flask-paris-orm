from instance.database import db
from models.car import CarRent


def create_car_rent(
    car_id,
    customer_name,
    customer_phone,
    rent_start,
    rent_end,
    hourly_rate: float = 100,
):
    """Create a car rent."""
    car_rent = CarRent(
        car_id=car_id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        hourly_rate=hourly_rate,
        rent_start=rent_start,
        rent_end=rent_end,
    )
    db.session.add(car_rent)
    db.session.commit()
    return car_rent
