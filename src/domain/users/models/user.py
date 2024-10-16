from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.infrastructure.database.models.base import Base
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="patron")
    is_active = Column(Boolean, default=True)

    borrow_history = relationship("Borrow", backref="user")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)