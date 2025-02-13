from sqlalchemy import Column, Integer, String , Boolean
from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(60), nullable=True)  # Required (manual) & optional (google auth)
    google_id = Column(String(100), unique=True, nullable=True)  # Required (google auth) & optional (manual)

    #optional field
    phone_no = Column(Integer, unique=True, nullable=True)
    age = Column(Integer, nullable=True)
    is_profile_complete = Column(Boolean, default = False)

    def __repr__(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
        }