from datetime import datetime

from instance.database import db
from shared import chrono


# ORM
class CarItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    brand: str = db.Column(db.String(50))
    license_plate: str = db.Column(db.String(20), unique=True)
    frame_number: str = db.Column(db.String(250), unique=True)
    model: str = db.Column(db.String(150))
    color: str = db.Column(db.String(50), nullable=True)
    created_at: datetime = db.Column(db.DateTime,default=chrono.now)
    updated_at: datetime = db.Column(db.DateTime, default=chrono.now, onupdate=chrono.now)