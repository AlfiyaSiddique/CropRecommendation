from sqlalchemy import Column, Integer, String
from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(60), nullable=True)  # Optional for Google auth
    google_id = Column(String(100), unique=True, nullable=True)  # Optional for manual process
    username = Column(String(100), unique=True)
    phone_no = Column(String(15), unique=True, nullable=True)  # Optional, can be left empty

    # Add more columns here

    def __repr__(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            # 'google_id': self.google_id,
            # 'phone_no': self.phone_no,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }