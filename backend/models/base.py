from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # This is abstract model and won't create a table

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    

#Add common attributes like createdat, updatesat in this model
