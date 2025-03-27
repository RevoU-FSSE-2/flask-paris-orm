from typing import Optional, List
from sqlalchemy.exc import IntegrityError

from models.users import User
from instance.database import db


class UserRepository:
    """Repository for User model operations"""

    @staticmethod
    def create_user(
        name: str, email: str, password: str
    ) -> tuple[User, bool, Optional[str]]:
        """
        Create a new user

        Args:
            name: User's full name
            email: User's email address
            password: User's plain text password

        Returns:
            tuple: (User object or None, success boolean, error message or None)
        """
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return None, False, "User with this email already exists"

        # Create new user
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user, True, None
        except IntegrityError:
            db.session.rollback()
            return None, False, "Database integrity error"
        except Exception as e:
            db.session.rollback()
            return None, False, str(e)

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.session.get(User, user_id)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all_users() -> List[User]:
        """Get all users"""
        return User.query.all()

    @staticmethod
    def update_user(
        user_id: int, **kwargs
    ) -> tuple[Optional[User], bool, Optional[str]]:
        """
        Update user details

        Args:
            user_id: The ID of the user to update
            **kwargs: Key-value pairs of attributes to update

        Returns:
            tuple: (Updated User object or None, success boolean, error message or None)
        """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None, False, f"User with ID {user_id} not found"

        # Update allowed fields
        allowed_fields = ["name", "email"]
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(user, field, value)
            elif field == "password":
                user.set_password(value)

        try:
            db.session.commit()
            return user, True, None
        except IntegrityError:
            db.session.rollback()
            return None, False, "Database integrity error"
        except Exception as e:
            db.session.rollback()
            return None, False, str(e)

    @staticmethod
    def delete_user(user_id: int) -> tuple[bool, Optional[str]]:
        """
        Delete a user

        Args:
            user_id: The ID of the user to delete

        Returns:
            tuple: (success boolean, error message or None)
        """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return False, f"User with ID {user_id} not found"

        try:
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def authenticate_user(
        email: str, password: str
    ) -> tuple[Optional[User], bool, Optional[str]]:
        """
        Authenticate a user with email and password

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            tuple: (User object or None, success boolean, error message or None)
        """
        user : User| None = UserRepository.get_user_by_email(email)
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user
