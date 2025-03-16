from sqlalchemy import Column, Integer, String , Boolean
from .base import BaseUser
from sqlalchemy.orm import relationship

class Farmer(BaseUser):
    __tablename__ = 'Farmers'

    # relation with product
    products = relationship("Product", back_populates="creator")

    def __repr__(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
        }