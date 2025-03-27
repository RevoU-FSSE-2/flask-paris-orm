from config.settings import create_app
from instance.database import db  # noqa: F401
import os
from flask_jwt_extended import get_jwt_identity, jwt_required
os.environ.setdefault("FLASK_CONFIG", "config.local")
config_module = os.getenv("FLASK_CONFIG")

app = create_app(config_module)

@app.before_request
@jwt_required(optional=True)
def user_middleware():
    """Check if JWT is decoded before each request"""
    user_id = get_jwt_identity()
    if user_id:
        # query the user from the database
        # inject the user into the request context
        print("User ID from JWT:", user_id)
   
   
