from flask import jsonify
from datetime import datetime
from . model import User, Item, Variant, Property, Activity, db
from tracker import app

'''
Mapping between activity type and user action
'''
actions = {0: "created", 1: "edited", 2: "deleted"}


@app.route('/activity/<username>/<from_date>/<to_date>', methods=['GET'])
def show_activity(username, from_date, to_date):
    users = {}
    from_timestamp = datetime.strptime(from_date, '%d-%m-%Y')
    to_timestamp = datetime.strptime(to_date, '%d-%m-%Y')
    activities = Activity.query.filter(Activity.username == username).filter(
        Activity.created_timestamp >= from_timestamp).filter(Activity.created_timestamp < to_timestamp).all()
    for activity in activities:
        event = {}
        event['action'] = actions.get(activity.type)
        event['item'] = activity.item_name
        event['variant'] = activity.variant_name
        event['property'] = activity.property_key
        event['timestamp'] = activity.created_timestamp
        if activity.username in users:
            users[activity.username].append(event)
        else:
            events = [event]
            users[activity.username] = events
    return jsonify(users=users)


@app.route('/activity/all/<from_date>/<to_date>', methods=['GET'])
def show_all_activity(from_date, to_date):
    users = {}
    from_timestamp = datetime.strptime(from_date, '%d-%m-%Y')
    to_timestamp = datetime.strptime(to_date, '%d-%m-%Y')
    activities = Activity.query.filter(Activity.created_timestamp >= from_timestamp).filter(
        Activity.created_timestamp < to_timestamp).all()
    for activity in activities:
        event = {}
        event['action'] = actions.get(activity.type)
        event['item'] = activity.item_name
        event['variant'] = activity.variant_name
        event['property'] = activity.property_key
        event['timestamp'] = activity.created_timestamp
        if activity.username in users:
            users[activity.username].append(event)
        else:
            events = [event]
            users[activity.username] = events
    return jsonify(users=users)


@app.route('/user/<username>/<first_name>/<last_name>/<email_id>', methods=['POST'])
def add_user(first_name, last_name, username, email_id):
    user = User(first_name, last_name, username, email_id)
    db.session.add(user)
    db.session.commit()
    return jsonify(Message='User added successfully')


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    results = list()
    user = User.query.filter_by(username=username).first()
    result = {}
    result['id'] = user.id
    result['username'] = user.username
    result['first_name'] = user.first_name
    result['last_name'] = user.last_name
    result['email_id'] = user.email_id
    result['created_timestamp'] = user.created_timestamp
    results.append(result)
    return jsonify(results)


@app.route('/user/all', methods=['GET'])
def get_all_user():
    results = list()
    users = User.query.all()
    for user in users:
        result = {}
        result['id'] = user.id
        result['username'] = user.username
        result['first_name'] = user.first_name
        result['last_name'] = user.last_name
        result['email_id'] = user.email_id
        result['created_timestamp'] = user.created_timestamp
        results.append(result)
    return jsonify(results)


@app.route('/item/<name>/<brand>/<product_code>/<category>', methods=['POST'])
def add_item(name, brand, product_code, category):
    item = Item(name, brand, product_code, category)
    db.session.add(item)
    db.session.commit()
    return jsonify(Message='Item added successfully')


@app.route('/item/<product_code>', methods=['GET'])
def get_item(product_code):
    results = list()
    item = Item.query.filter_by(product_code=product_code).first()
    result = {}
    result['id'] = item.id
    result['name'] = item.name
    result['brand'] = item.brand
    result['product_code'] = item.product_code
    result['category'] = item.category
    result['created_timestamp'] = item.created_timestamp
    results.append(result)
    return jsonify(results)


@app.route('/item/all', methods=['GET'])
def get_all_item():
    results = list()
    items = Item.query.all()
    for item in items:
        result = {}
        result['id'] = item.id
        result['name'] = item.name
        result['brand'] = item.brand
        result['product_code'] = item.product_code
        result['category'] = item.category
        result['created_timestamp'] = item.created_timestamp
        results.append(result)
    return jsonify(results)


@app.route('/variant/<name>/<selling_price>/<cost_price>/<quantity>/<product_code>', methods=['POST'])
def add_variant(name, selling_price, cost_price, quantity, product_code):
    item = Item.query.filter_by(product_code=product_code).first()
    variant = Variant(name, selling_price, cost_price, quantity, item.id)
    db.session.add(variant)
    db.session.commit()
    return jsonify(Message='Variant added successfully')


@app.route('/variant/<product_code>', methods=['GET'])
def get_variant(product_code):
    results = list()
    item = Item.query.filter_by(product_code=product_code).first()
    variants = Variant.query.filter_by(item_id=item.id).all()
    for variant in variants:
        result = {}
        result['id'] = variant.id
        result['name'] = variant.name
        result['selling_price'] = variant.selling_price
        result['cost_price'] = variant.cost_price
        result['quantity'] = variant.quantity
        result['created_timestamp'] = variant.created_timestamp
        results.append(result)
    return jsonify(results)


@app.route('/variant/<variant_id>/property/<key>/<value>/<username>', methods=['POST'])
def add_variant_property(variant_id, key, value, username):
    property = Property(key, value, variant_id)
    db.session.add(property)
    db.session.commit()
    variant = Variant.query.filter_by(id=variant_id).first()
    item = Item.query.filter_by(id=variant.item_id).first()
    activity = Activity(0, username, item.name, variant.name, property.key)
    db.session.add(activity)
    db.session.commit()
    return jsonify(Message='Property added successfully')


@app.route('/variant/<variant_id>/property', methods=['GET'])
def get_variant_property(variant_id):
    results = list()
    properties = Property.query.filter_by(variant_id=variant_id).all()
    for property in properties:
        result = {}
        result['id'] = property.id
        result['key'] = property.key
        result['value'] = property.value
        result['created_timestamp'] = property.created_timestamp
        results.append(result)
    return jsonify(results)


@app.route('/variant/<variant_id>/property/<key>/<old_value>/<new_value>/<username>', methods=['PUT'])
def edit_variant_property(variant_id, key, old_value, new_value, username):
    property = Property.query.filter(Property.variant_id == variant_id).filter(Property.key == key).filter(
        Property.value == old_value).first()
    property.value = new_value
    db.session.commit()
    variant = Variant.query.filter_by(id=variant_id).first()
    item = Item.query.filter_by(id=variant.item_id).first()
    activity = Activity(1, username, item.name, variant.name, property.key)
    db.session.add(activity)
    db.session.commit()
    return jsonify(Message='Property modified successfully')


@app.route('/variant/<variant_id>/property/<key>/<value>/<username>', methods=['DELETE'])
def delete_variant_property(variant_id, key, value, username):
    property = Property.query.filter(Property.variant_id == variant_id).filter(Property.key == key).filter(
        Property.value == value).first()
    db.session.delete(property)
    db.session.commit()
    variant = Variant.query.filter_by(id=variant_id).first()
    item = Item.query.filter_by(id=variant.item_id).first()
    activity = Activity(2, username, item.name, variant.name, property.key)
    db.session.add(activity)
    db.session.commit()
    return jsonify(Message='Property removed successfully')


if __name__ == '__main__':
    app.run()
