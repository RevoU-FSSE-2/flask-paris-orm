from config.settings import create_app
from instance.database import db  # noqa: F401

app = create_app("config.local")
