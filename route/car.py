from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError

from repo.car import create_car_item


class CarItemRequest(BaseModel):
    brand: str
    license_plate: str
    frame_number: str
    model: str
    color: str


car_router = Blueprint("car", __name__, url_prefix="/car")


@car_router.route("", methods=["POST"])
def create_car():
    """rented route."""

    data = request.json
    try:
        car = CarItemRequest.model_validate(data)
    except ValidationError as e:
        return jsonify(
            {
                "success": False,
                "data": e.errors(include_url=False, include_context=False, include_input=False),
            }
        ), 400
    created_car = create_car_item(
        car.brand, car.license_plate, car.frame_number, car.model, car.color
    )
    return jsonify(
        {
            "data": {
                "brand": created_car.brand,
                "id": created_car.id,
            },
            "success": True,
        }
    ), 201
