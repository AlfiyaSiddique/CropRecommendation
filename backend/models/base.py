from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # This is abstract model and won't create a table

#Add common attributes like createdat, updatesat in this model
