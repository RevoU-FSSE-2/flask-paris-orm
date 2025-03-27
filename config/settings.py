from flask import Flask
import models  # noqa: F401
from instance.database import init_db
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from route.car import car_router
from route.index import index_router
from route.rent import rent_router
from route.user import user_router
from repo.user import UserRepository


def create_app(config_module="config.local"):
    app = Flask(__name__)
    app.config.from_object(config_module)
    init_db(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    jwt = JWTManager(app)
    app.register_blueprint(index_router)
    app.register_blueprint(rent_router)
    app.register_blueprint(car_router)
    app.register_blueprint(user_router)

    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.get_user_by_id(int(user_id))

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)

    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_payload):
        user_id = jwt_payload["sub"]
        user = UserRepository.get_user_by_id(user_id)
        return user

    return app
