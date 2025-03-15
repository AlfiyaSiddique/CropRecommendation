from sqlalchemy import Column , String , Integer , ForeignKey
from .base import BaseModel
from sqlalchemy.orm import relationship

class Product(BaseModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement = True)
    product_name = Column(String(200), nullable=False)
    product_desc = Column(String(200),nullable=False)
    price = Column(Integer, nullable = False )
    image_url = Column(String(200), nullable=False)

    user_id = Column(Integer, ForeignKey('Farmers.id'), nullable=False)

    creator = relationship("Farmer", back_populates="products")

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_desc': self.product_desc,
            'price': self.price,
            'user_id': self.user_id
        }