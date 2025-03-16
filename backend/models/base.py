from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # This is abstract model and won't create a table

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    

#Add common attributes like createdat, updatesat in this model

class BaseUser(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(60), nullable=True)  # Required ( for manual) & optional ( for Google auth)
    google_id = Column(String(100), unique=True, nullable=True)  # Optional for Google authentication

    # Optional fields
    phone_no = Column(String(15), unique=True, nullable=True)
    is_profile_complete = Column(Boolean, default=False)