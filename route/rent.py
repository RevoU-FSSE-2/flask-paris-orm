from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError, computed_field

from instance.database import db
from models.car import CarItem, CarRent
from repo.rent import create_car_rent
from shared import chrono


class RentItemRequest(BaseModel):
    car_id: int
    customer_name: str
    customer_phone: str
    days: int

    @computed_field
    def rent_start(self) -> chrono.datetime:
        return chrono.now()

    @computed_field
    def rent_end(self) -> chrono.datetime:
        return chrono.forward_days(self.days)


rent_router = Blueprint("rent", __name__, url_prefix="/rent")


@rent_router.route("", methods=["GET"])
def get_rented_car():
    car_rented = db.session.query(CarRent).all() # query N+1
    response = []
    for car_rent in car_rented:
        response.append(
            {
                "car": car_rent.car.brand,
                "customer_name": car_rent.customer_name,
                "customer_phone": car_rent.customer_phone,
                "rent_start": car_rent.rent_start,
                "rent_end": car_rent.rent_end,
                "status": str(car_rent.status),
            }
        )
    return jsonify(
        {
            "success": True,
            "data": response,
        }
    ), 200


@rent_router.route("", methods=["POST"])
def rent_car():
    """rented route."""
    try:
        rent = RentItemRequest.model_validate(request.json)
    except ValidationError as e:
        return jsonify(
            {
                "success": False,
                "data": e.errors(
                    include_url=False, include_context=False, include_input=False
                ),
            }
        ), 400
    _ = db.get_or_404(CarItem, rent.car_id)
    car_rent = create_car_rent(
        rent.car_id,
        rent.customer_name,
        rent.customer_phone,
        rent.rent_start,
        rent.rent_end,
    )
    return jsonify(
        {
            "success": True,
            "data": {
                "rent_id": car_rent.id,
                "status": str(car_rent.status),
            },
        }
    ), 201
