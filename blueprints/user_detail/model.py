from blueprints import db 
from flask_restful import fields

class UserDetail(db.Model):
    __tablename__ = "user_detail"
    user_id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(255), nullable = False)
    address = db.Column(db.String(255), nullable = True)
    phone = db.Column(db.String(20), nullable = True)

    response_fields = {
        'user_id':fields.Integer,
        'full_name':fields.String,
        'address':fields.String,
        'phone':fields.String
    }

    def __init__(self, user_id, full_name, address, phone):
        self.user_id = user_id
        self.full_name = full_name
        self.address = address
        self.phone = phone
