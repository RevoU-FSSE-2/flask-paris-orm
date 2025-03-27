from flask import Flask
import models  # noqa: F401
from instance.database import init_db
from middlewares.authmiddleware import init as init_middleware
from flask_jwt_extended import JWTManager
from route.car import car_router
from route.index import index_router
from route.rent import rent_router
from route.user import user_router


def create_app(config_module="config.local"):
    app = Flask(__name__)
    app.config.from_object(config_module)
    init_db(app)
    init_middleware(app)
    jwt = JWTManager(app)
    app.register_blueprint(index_router)
    app.register_blueprint(rent_router)
    app.register_blueprint(car_router)
    app.register_blueprint(user_router)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)
    return app
