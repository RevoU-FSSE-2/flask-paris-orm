from datetime import datetime
from enum import Enum

from instance.database import db
from shared import chrono


class RentStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


# ORM
class CarItem(db.Model):
    __tablename__ = "car_item"
    id: int = db.Column(db.Integer, primary_key=True)
    brand: str = db.Column(db.String(50))
    license_plate: str = db.Column(db.String(20), unique=True)
    frame_number: str = db.Column(db.String(250), unique=True)
    model: str = db.Column(db.String(150))
    color: str = db.Column(db.String(50), nullable=True)
    created_at: datetime = db.Column(db.DateTime, default=chrono.now)
    updated_at: datetime = db.Column(
        db.DateTime, default=chrono.now, onupdate=chrono.now
    )

    def __repr__(self):
        return f"ID: {self.id} | brand: {self.brand} -> {self.license_plate}"


class CarRent(db.Model):
    __tablename__ = "car_rent"
    id: int = db.Column(db.Integer, primary_key=True)
    car = db.relationship("CarItem", backref="rents", lazy=True)
    car_id: int = db.Column(db.Integer, db.ForeignKey("car_item.id"), nullable=False)
    customer_name: str = db.Column(db.String(150))
    customer_phone: str = db.Column(db.String(20))
    rent_start: datetime = db.Column(db.DateTime)
    rent_end: datetime = db.Column(db.DateTime)
    created_at: datetime = db.Column(db.DateTime, default=chrono.now)
    updated_at: datetime = db.Column(
        db.DateTime, default=chrono.now, onupdate=chrono.now
    )
    hourly_rate: float = db.Column(db.Float)
    status: RentStatus = db.Column(db.Enum(RentStatus), default=RentStatus.ACTIVE)
