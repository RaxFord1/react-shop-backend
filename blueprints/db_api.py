from flask import jsonify, request, Blueprint

from database.database import Session, Category, Item, OrderItem, Favourite, User, Order

dbAPI = Blueprint('simple_page', __name__, template_folder='templates')


# Add a new category
@dbAPI.route('/category', methods=['POST'])
def add_category():
    session = Session()
    category_name = request.json['name']
    category = Category(name=category_name)
    session.add(category)
    session.commit()
    session.refresh(category)
    session.close()

    return jsonify({'message': 'Category added successfully', 'id': category.id})


@dbAPI.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    session = Session()
    category = session.query(Category).get(category_id)
    if category:
        session.delete(category)
        session.commit()
        session.close()
        return jsonify({'message': 'Category deleted successfully'})
    else:
        session.close()
        return jsonify({'error': f'Category with ID {category_id} not found'}), 404


# Add a new item
@dbAPI.route('/item', methods=['POST'])
def add_item():
    session = Session()
    item_name = request.json['name']
    item_description = request.json['description']
    item_image_url = request.json['image_url']
    item_category_id = request.json['category_id']
    item_on_sale = request.json['on_sale']
    item = Item(name=item_name, description=item_description, image_url=item_image_url,
                category_id=item_category_id, on_sale=item_on_sale)
    session.add(item)
    session.commit()
    session.refresh(item)
    session.close()

    return jsonify({'message': 'Item added successfully', 'id': item.id})


# Delete an item by ID
@dbAPI.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    session = Session()
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
        session.close()
        return jsonify({'message': 'Item deleted successfully'})
    else:
        session.close()
    return jsonify({'error': f'Item with ID {item_id} not found'}), 404


# Add a new order item
@dbAPI.route('/order_item', methods=['POST'])
def add_order_item():
    session = Session()
    order_id = request.json['order_id']
    item_id = request.json['item_id']
    order_item = OrderItem(order_id=order_id, item_id=item_id)
    session.add(order_item)
    session.commit()
    session.close()
    return jsonify({'message': 'Order item added successfully'})


# Delete an order item by order ID and item ID
@dbAPI.route('/order_item/<int:order_id>/<int:item_id>', methods=['DELETE'])
def delete_order_item(order_id, item_id):
    session = Session()
    order_item = session.query(OrderItem).filter_by(order_id=order_id, item_id=item_id).first()
    if order_item:
        session.delete(order_item)
        session.commit()
        session.close()
        return jsonify({'message': 'Order item deleted successfully'})
    else:
        session.close()
        return jsonify({'error': f'Order item with order ID {order_id} and item ID {item_id} not found'}), 404


# Add a new favourite
@dbAPI.route('/favourite', methods=['POST'])
def add_favourite():
    session = Session()
    item_id = request.json['item_id']
    user_id = request.json['user_id']
    favourite = Favourite(item_id=item_id, user_id=user_id)
    session.add(favourite)
    session.commit()
    session.close()
    return jsonify({'message': 'Favourite added successfully'})


@dbAPI.route('/favourite/<int:favourite_id>', methods=['DELETE'])
def delete_favourite(favourite_id):
    session = Session()
    favourite = session.query(Favourite).filter_by(id=favourite_id).first()
    if favourite:
        session.delete(favourite)
        session.commit()
        session.close()
        return jsonify({'message': 'Favourite deleted successfully'})
    else:
        session.close()
        return jsonify({'error': f'Favourite with ID {favourite_id} not found'}), 404


@dbAPI.route('/user', methods=['POST'])
def add_user():
    session = Session()
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password_hash = request.json['password_hash']
    user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.close()
    return jsonify({'message': 'User added successfully'})


@dbAPI.route('/order', methods=['POST'])
def add_order():
    session = Session()
    user_id = request.json['user_id']
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    session.close()
    return jsonify({'message': 'Order added successfully'})
