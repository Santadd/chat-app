#import the SQLAlchemy class
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#Define a class for the Database
class User(UserMixin, db.Model):
    """User model"""
    #Explicitly define the tablename
    __tablename__ = "users"
    #Define the table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    