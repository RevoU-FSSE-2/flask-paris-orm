import faker
from faker_vehicle import VehicleProvider

from config.settings import create_app
from instance.database import db
from models.car import CarItem

app = create_app("config.local")
fake = faker.Faker()
fake.add_provider(VehicleProvider)


def create_fake_car_items():
    with app.app_context():
        car_items = []
        for _ in range(10):
            car_item = CarItem(
                brand=fake.vehicle_make(),
                license_plate=fake.license_plate(),
                frame_number=fake.uuid4(),
                model=fake.vehicle_model(),
                color=fake.color_name(),
            )
            car_items.append(car_item)
        print("INSERTING TO DB")
        db.session.add_all(car_items)
        db.session.commit()
        print("INSERTED")
        return car_items
