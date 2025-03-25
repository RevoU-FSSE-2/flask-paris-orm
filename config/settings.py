from flask import Flask

import models  # noqa: F401
from instance.database import init_db
from route.car import car_router
from route.index import index_router
from route.rent import rent_router


def create_app(config_module="config.local"):
    app = Flask(__name__)
    app.config.from_object(config_module)
    init_db(app)
    app.register_blueprint(index_router)
    app.register_blueprint(rent_router)
    app.register_blueprint(car_router)
    return app
