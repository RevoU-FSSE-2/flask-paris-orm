from flask import Blueprint, jsonify, request
from pydantic import BaseModel, EmailStr, field_validator
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

from middlewares.authmiddleware import login_required, staff_only
from repo.user import UserRepository

user_router = Blueprint("user", __name__, url_prefix="/users")


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@user_router.route("", methods=["POST"])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        user_data = UserCreateRequest(**data)
    except Exception as e:
        return jsonify(
            {"success": False, "message": "Invalid request data", "errors": str(e)}
        ), 400

    # Use repository to create user
    user, success, error = UserRepository.create_user(
        name=user_data.name, email=user_data.email, password=user_data.password
    )

    if not success:
        # Handle specific error cases
        if "already exists" in error:
            return jsonify({"success": False, "message": error}), 400
        return jsonify({"success": False, "message": error}), 400

    return jsonify(
        {
            "success": True,
            "message": "User created successfully",
            "data": user.serialize,
        }
    ), 201


@user_router.route("/login", methods=["POST"])
def login():
    """Login with email and password, supporting both session and JWT authentication"""
    try:
        data = request.json
        login_data = LoginRequest.model_validate(data)
    except Exception as e:
        return jsonify(
            {"success": False, "message": "Invalid request data", "errors": str(e)}
        ), 400

    # Authenticate user
    user = UserRepository.authenticate_user(
        email=login_data.email, password=login_data.password
    )
    if not user:
        return jsonify({"success": False, "message": "authentication failed"}), 401
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    return jsonify(
        {
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        }
    ), 200
   



@user_router.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh JWT access token"""
    current_user_id = get_jwt_identity()
    user = UserRepository.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"success": False, "message": "invalid refresh token"}), 401

    access_token = create_access_token(identity=user)
    return jsonify({"success": True, "data": {"access_token": access_token}}), 200


@user_router.route("/me", methods=["GET"])
@login_required
def get_current_user_jwt():
    """Get current user details (JWT authentication)"""
    return jsonify({"success": True, "data": request.user.serialize}), 200

@user_router.route("/secret-user", methods=["GET"])
@login_required
@staff_only
def secret_message_from_staff():
    """A secret message route"""
    return jsonify({"success": True, "message": f"This is a secret message for {request.user.name}"}), 200
