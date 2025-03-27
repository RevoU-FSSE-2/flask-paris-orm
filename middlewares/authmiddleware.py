from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify
from models import User
from repo.user import UserRepository
from functools import wraps

def init(app):
    """Initialize the app with middleware"""
    @app.before_request
    @jwt_required(optional=True)
    def user_injector_middleware():
        user_id = get_jwt_identity()
        user = None
        if user_id:
            user : User | None = UserRepository.get_user_by_id(user_id)

        request.user = user

def login_required(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.user:
            return jsonify({"success": False, "message": "not authenticated"}), 401
        return f(*args, **kwargs)
    return wrapper

def staff_only(f):
    """Decorator to require login for a route"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.user.is_staff:
            return jsonify({"success": False, "message": "not Authorized, staff only"}), 403
        return f(*args, **kwargs)
    return wrapper