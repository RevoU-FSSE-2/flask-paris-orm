from .base import *  # noqa: F401, F403

SQLALCHEMY_DATABASE_URI = (
    "postgresql://autoshop-user:BrollyV543@localhost:5444/dealer_db"
)
JWT_ACCESS_TOKEN_EXPIRES = 180 # 3 minutes