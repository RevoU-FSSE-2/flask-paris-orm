from config.settings import create_app
from instance.database import db  # noqa: F401
import os

os.environ.setdefault("FLASK_CONFIG", "config.local")
config_module = os.getenv("FLASK_CONFIG")

app = create_app(config_module)
