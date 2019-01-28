from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tracker import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, index=True)
    email_id = db.Column(db.String(50), unique=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, first_name, last_name, username, email_id):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email_id = email_id


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    product_code = db.Column(db.String(50), unique=True, index=True)
    category = db.Column(db.String(50))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, brand, product_code, category):
        self.name = name
        self.brand = brand
        self.product_code = product_code
        self.category = category


class Variant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    selling_price = db.Column(db.Float)
    cost_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, selling_price, cost_price, quantity, item_id):
        self.name = name
        self.selling_price=selling_price
        self.cost_price = cost_price
        self.quantity = quantity
        self.item_id = item_id


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(50))
    value = db.Column(db.String(50))
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, key, value, variant_id):
        self.key = key
        self.value = value
        self.variant_id = variant_id


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer)
    username = db.Column(db.String(50))
    item_name = db.Column(db.String(50))
    variant_name = db.Column(db.String(50))
    property_key = db.Column(db.String(50))
    created_timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, type, username, item_name, variant_name, property_key):
        self.type = type
        self.username = username
        self.item_name = item_name
        self.variant_name = variant_name
        self.property_key = property_key


db.create_all()
