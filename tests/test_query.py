from models.car import CarItem


def test_car_item_query(db, cars):
    """Test the car item query."""
    # dia sebagai query builder
    query = db.select(CarItem).where(CarItem.license_plate == "B20AG").limit(1)
    print(query)
    """
    SELECT car_item.id, car_item.brand, car_item.license_plate, car_item.frame_number, car_item.model, car_item.color, car_item.created_at, car_item.updated_at 
    FROM car_item 
    WHERE car_item.license_plate = :license_plate_1
    LIMIT :param_1
    """
    car = db.session.execute(query).scalar_one()
    # <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7efd6d9a0050>
    # select * from CarItem where license_plate = 'B20AG' limit 1;
    assert car.brand == "TOYOTA"
    
