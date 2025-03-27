from .base import *  # noqa: F401, F403

TESTING = True
# command untuk run
# SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
SQLALCHEMY_DATABASE_URI = (
    "postgresql://autoshop-user:BrollyV543@localhost:5444/test_dealer_db"
)
