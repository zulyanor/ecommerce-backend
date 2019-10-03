from blueprints import db
from flask_restful import fields
from datetime import datetime

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, nullable = False)
    category_id = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(255), nullable = False)
    stock = db.Column(db.Integer, nullable = False, default = 1)
    price = db.Column(db.Integer, nullable = False) 
    location = db.Column(db.String(100), nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable =False)
    image_url = db.Column(db.String(1000), nullable = False)
    status = db.Column(db.Integer, nullable = False) # 1 for new 0 for second
    discount = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.DateTime, nullable = False)

    response_fields = {
        'id':fields.Integer, 
        'user_id':fields.Integer,
        'category_id':fields.Integer,
        'name':fields.String,
        'stock':fields.Integer,
        'price':fields.Integer,
        'location':fields.String,
        'weight':fields.Integer,
        'description':fields.String,
        'image_url':fields.String,
        'status':fields.Integer,
        'discount':fields.Integer,
        'created_at':fields.DateTime
    }

    data = {
        'user_id': 0,
        'category_id': 0,
        'name': 'Product',
        'stock': 0,
        'price': 0,
        'location': 'Location',
        'image_url': 'url',
        'discount': 0,
        'status': 0
    }

    def __init__(self, data):
        self.user_id = data['user_id']
        self.category_id = data['category_id']
        self.name = data['name']
        self.stock = data['stock']
        self.price = data['price']
        self.location = data['location']
        self.weight = data['weight']
        self.description = data['description']
        self.image_url = data['image_url']
        self.status = data['status']
        self.discount = data['discount']
        self.created_at = datetime.utcnow()