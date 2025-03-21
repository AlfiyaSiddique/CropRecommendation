from sqlalchemy import Column, Integer, String , Boolean
from .base import BaseUser

class User(BaseUser):
    __tablename__ = 'Users'

    #optional field
    age = Column(Integer, nullable=True)

    def __repr__(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
        }