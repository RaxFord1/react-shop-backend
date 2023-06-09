from datetime import datetime

from flask import jsonify, request, Blueprint, make_response
from sqlalchemy import desc

from database.database import Session, Category, Item, OrderItem, Favourite, User, Order, Review

dbAPI = Blueprint('db_api', __name__, template_folder='templates')


@dbAPI.route('/categories', methods=['GET'])
def get_categories():
    session = Session()
    items = session.query(Category).all()
    session.close()

    if not items:
        return jsonify({'message': 'No categories found', items: []})

    item_list = []
    for item in items:
        item_list.append({
            'id': item.id,
            'name': item.name,
            'value': item.value
        })

    return jsonify({'items': item_list})


# Add a new category
@dbAPI.route('/category', methods=['POST'])
def add_category():
    session = Session()
    category_name = request.json['label']
    category_value = request.json['value']
    category = Category(name=category_name, value=category_value)
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


@dbAPI.route('/items', methods=['GET'])
def get_items():
    session = Session()
    items = session.query(Item).all()
    session.close()

    if not items:
        return jsonify({'message': 'No items found'})

    item_list = []
    for item in items:
        item_list.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'image_url': item.image_url,
            'category_id': item.category_id,
            'on_sale': item.on_sale,
            'price': item.price
        })

    return jsonify({'items': item_list})


# Add a new item
@dbAPI.route('/item', methods=['POST'])
def add_item():
    session = Session()
    item_name = request.json['name']
    item_description = request.json['description']
    item_image_url = request.json['image']
    item_category = request.json['category']
    item_on_sale = request.json['on_sale']
    item_price = request.json['price']
    item_category_id = session.query(Category.id).filter_by(value=item_category).first()
    if item_category_id is None:
        item_category_id = session.query(Category.id).filter_by(name=item_category).first()
        if item_category_id is None:
            print(f"{item_category = }")
            return make_response({'message': 'Unknown category!'}, 400)
    item_category_id = item_category_id[0]
    item = Item(name=item_name, description=item_description, image_url=item_image_url,
                category_id=item_category_id, on_sale=item_on_sale, price=item_price)
    session.add(item)
    session.commit()
    session.refresh(item)
    session.close()

    return jsonify({'message': 'Item added successfully', 'id': item.id})


# Update an item
@dbAPI.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    session = Session()
    item = session.query(Item).get(item_id)

    if not item:
        session.close()
        return jsonify({'message': 'Item not found'})

    item.name = request.json.get('name', item.name)
    item.description = request.json.get('description', item.description)
    item.image_url = request.json.get('image', item.image_url)
    item_category = request.json.get('category', None)
    if item_category is None:
        item.category_id = request.json.get('category_id', item.category_id)
    else:
        item_category_id = session.query(Category.id).filter_by(value=item_category).first()
        if item_category_id is None:
            item_category_id = session.query(Category.id).filter_by(name=item_category).first()
            if item_category_id is None:
                print(f"{item_category = }")
                return make_response({'message': 'Unknown category!'}, 400)
        item.category_id = item_category_id[0]
    item.on_sale = request.json.get('on_sale', item.on_sale)
    item.price = request.json.get('price', item.price)

    session.commit()
    session.close()

    return jsonify({'message': 'Item updated successfully'})


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


@dbAPI.route('/favourite/<int:user_id>/<int:item_id>', methods=['DELETE'])
def delete_favourite(user_id, item_id):
    session = Session()
    favourite = session.query(Favourite).filter_by(item_id=item_id, user_id=user_id).first()
    if favourite:
        session.delete(favourite)
        session.commit()
        session.close()
        return jsonify({'message': 'Favourite deleted successfully'})
    else:
        session.close()
        return jsonify({'error': f'Favourite with ID {item_id = }, {user_id = } not found'}), 404


@dbAPI.route('/favourite/<int:user_id>', methods=['GET'])
def get_favourite(user_id):
    session = Session()
    favorites = session.query(Favourite).filter_by(user_id=user_id).all()
    if not favorites:
        return jsonify({'message': 'No favorites found for the user'})

    favorite_items = []
    for favorite in favorites:
        # favorite_items.append({
        #     'id': favorite.id,
        #     'item_id': favorite.item_id,
        #     'user_id': favorite.user_id
        # })
        favorite_items.append(favorite.item_id)

    return jsonify({'favorites': favorite_items})


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


def get_or_create_last_unpaid_order(user_id):
    session = Session()
    last_unpaid_order = session.query(Order).filter(
        Order.user_id == user_id, Order.paid == False
    ).order_by(desc(Order.id)).first()
    if last_unpaid_order:
        order_id = last_unpaid_order.id
        session.commit()
        session.close()
        return order_id
    else:
        new_order = Order(user_id=user_id)
        session.add(new_order)
        session.flush()
        order_id = new_order.id
        session.commit()
        session.close()
        return order_id


@dbAPI.route('/last_unpaid_order/<int:user_id>', methods=['GET'])
def last_unpaid_order_api(user_id):
    order_id = get_or_create_last_unpaid_order(user_id)
    if order_id is not None:
        return jsonify({'id': f'{order_id}'})

    return make_response({'message': 'Couldn\'t get last unpaid order! Maybe unknown user?'}, 400)


# Add a new order item
@dbAPI.route('/order_item', methods=['POST'])
def add_order_item():
    session = Session()
    user_id = request.json['user_id']
    item_id = request.json['item_id']
    # Get the last unpaid order with the maximum ID
    last_unpaid_order = get_or_create_last_unpaid_order(user_id)

    if last_unpaid_order:
        order_item = OrderItem(order_id=last_unpaid_order, item_id=item_id)
        session.add(order_item)
        session.commit()
        session.close()
        return jsonify({'message': 'Order item added successfully'})

    return make_response({'message': 'Couldn\'t add last unpaid order! Maybe unknown user?'}, 400)


# Add a new order item
@dbAPI.route('/order_items/<int:order_id>', methods=['GET'])
def get_order_items(order_id):
    session = Session()
    # Get the last unpaid order with the maximum ID
    order_items = session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    session.close()

    if not order_items:
        return jsonify({'message': 'No order_items found'})

    item_list = []
    for item in order_items:
        item_list.append({
            'item_id': item.item_id,
            'order_id': item.order_id
        })

    return jsonify({'items': item_list})


@dbAPI.route('/pay', methods=['POST'])
def pay_order():
    session = Session()
    order_id = request.json['order_id']
    # Retrieve the order by ID
    order = session.query(Order).filter(Order.id == order_id).first()

    if order:
        order.order_date = datetime.utcnow()
        order.paid = True

        session.commit()
        session.close()

        return jsonify({'message': 'Order has been marked as paid'})
    else:
        session.close()
        return jsonify({'message': 'Order not found'})


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


# Add a new review
@dbAPI.route('/review', methods=['POST'])
def add_review():
    session = Session()
    item_id = request.json['item_id']
    user_id = request.json['user_id']
    text = request.json['message']
    review = Review(text=text, item_id=item_id, user_id=user_id)
    session.add(review)
    session.commit()
    session.close()
    return jsonify({'message': 'Review added successfully'})


# Get a review on item
@dbAPI.route('/review/<int:item_id>', methods=['GET'])
def get_review(item_id):
    session = Session()
    # Get the last unpaid order with the maximum ID
    review_items: [Review] = session.query(Review).filter(Review.item_id == item_id).all()
    session.close()

    if not review_items:
        return jsonify({'message': 'No reviews found'})

    session = Session()
    item_list = []
    for item in review_items:
        user = session.query(User).filter(User.id == item.user_id).first()
        session.refresh(user)
        user_name = user.first_name + " " + user.last_name

        item_list.append({
            'text': item.text,
            'user_name': user_name
        })
    session.close()

    return jsonify({'items': item_list})
