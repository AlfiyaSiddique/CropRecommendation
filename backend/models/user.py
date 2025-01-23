from sqlalchemy import Column, Integer, String
from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    # Add more columns here

    def __repr__(self):
        return f"<User {self.username}>"
