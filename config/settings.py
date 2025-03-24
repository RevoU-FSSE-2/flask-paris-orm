from flask import Flask

import models  # noqa: F401
from instance.database import init_db
from route.index import index_router


def create_app(config_module="config.local"):
    app = Flask(__name__)
    app.config.from_object(config_module)
    init_db(app)
    app.register_blueprint(index_router)
    return app
