from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from instance.database import db
from shared import chrono

class User(db.Model, UserMixin):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=chrono.now)
    updated_at = db.Column(db.DateTime, default=chrono.now, onupdate=chrono.now)
    is_staff = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
    
    def set_password(self, password):
        """Set the password hash from a plaintext password"""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password, password)
        
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }