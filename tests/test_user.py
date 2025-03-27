import pytest
from models.users import User
from instance.database import db


def test_user_create(app):
    """Test creating a user and checking fields"""
    with app.app_context():
        test_user = User(
            name="Test User",
            email="test@example.com"
        )
        test_user.set_password("secure_password")
        
        db.session.add(test_user)
        db.session.commit()
        
        # Retrieve the user from database
        user = User.query.filter_by(email="test@example.com").first()
        
        assert user is not None
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.check_password("secure_password") is True
        assert user.check_password("wrong_password") is False


def test_user_serialize(app):
    """Test the serialize property of the User model"""
    with app.app_context():
        test_user = User(
            name="Serialize Test",
            email="serialize@example.com"
        )
        test_user.set_password("secure_password")
        
        db.session.add(test_user)
        db.session.commit()
        
        serialized = test_user.serialize
        
        assert "id" in serialized
        assert serialized["name"] == "Serialize Test"
        assert serialized["email"] == "serialize@example.com"
        assert "created_at" in serialized
        assert "updated_at" in serialized
        assert "password_hash" not in serialized


def test_user_unique_email(app):
    """Test that email must be unique"""
    with app.app_context():
        # Create first user
        user1 = User(
            name="User One",
            email="duplicate@example.com"
        )
        user1.set_password("password1")
        
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(
            name="User Two",
            email="duplicate@example.com"
        )
        user2.set_password("password2")
        
        db.session.add(user2)
        
        with pytest.raises(Exception):
            db.session.commit()
        
        db.session.rollback()