from blueprints import db
from flask_restful import fields
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    gender = db.Column(db.Integer, nullable = False)
    first_login_status = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)

    response_fields = {
        'id':fields.Integer,
        'username':fields.String,
        'email':fields.String,
        'password':fields.String,
        'gender':fields.Integer,
        'first_login_status':fields.Integer,
        'created_at':fields.DateTime
    }

    # to be put on jwt claims
    jwt_response_fields = {
        'id':fields.Integer,
        'username':fields.String
    }

    def __init__(self, username, email, password, gender):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.created_at = datetime.utcnow()
        