import unittest

from database.database import Session, OrderItem, Favourite, Item, Category, Order, User
from api.index import app

category_name = 'Clothing'

item_name = 'Red T-Shirt'
item_desc = 'A red cotton T-shirt in size medium'
item_img = 'https://example.com/images/red-tshirt.jpg'

user_first_name = 'John'
user_last_name = 'Doe'
user_email = 'johndoe@example.com'
user_password = 'password123'


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.session = Session()
        self.session.query(OrderItem).delete()
        self.session.query(Favourite).delete()
        self.session.query(Item).delete()
        self.session.query(Category).delete()
        self.session.query(Order).delete()
        self.session.query(User).delete()
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_add_category(self):
        response = self.client.post('/category', json={'name': 'Clothing'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Category added successfully')

    def test_add_item(self):
        category = Category(name=category_name)
        self.session.add(category)
        category_id, = self.session.query(Category.id).filter_by(name=category_name).first()
        self.session.commit()
        response = self.client.post('/item', json={
            'name': item_name,
            'description': item_desc,
            'image_url': item_img,
            'category_id': category_id,
            'on_sale': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item added successfully')

        response = self.client.delete(f'/item/{response.json["id"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item deleted successfully')

    def test_add_order(self):
        user = User(first_name='John', last_name='Doe', email='johndoe@example.com', password_hash='password123')
        self.session.add(user)
        user_id, = self.session.query(User.id).filter_by(first_name=user_first_name, last_name=user_last_name,
                                                         email=user_email, password_hash=user_password).first()
        self.session.commit()
        response = self.client.post('/order', json={'user_id': user_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Order added successfully'})

    def test_order_item(self):
        category = Category(name=category_name)
        self.session.add(category)
        category_id, = self.session.query(Category.id).filter_by(name=category_name).first()

        item = Item(name=item_name, description=item_desc,
                    image_url=item_img, category_id=category_id, on_sale=False)
        self.session.add(item)
        item_id, = self.session.query(Item.id).filter_by(name=item_name, description=item_desc,
                                                         image_url=item_img, category_id=category_id,
                                                         on_sale=False).first()

        user = User(first_name=user_first_name, last_name=user_last_name, email=user_email, password_hash=user_password)
        self.session.add(user)
        user_id, = self.session.query(User.id).filter_by(first_name=user_first_name, last_name=user_last_name,
                                                         email=user_email, password_hash=user_password).first()

        order = Order(user_id=user_id)
        self.session.add(order)
        order_id, = self.session.query(Order.id).filter_by(user_id=user_id).first()
        self.session.commit()
        response = self.client.post('/order_item', json={
            'order_id': order_id,
            'item_id': item_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Order item added successfully'})

        response = self.client.delete(f'/order_item/{order_id}/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Order item deleted successfully'})

    def test_favourite(self):
        category = Category(name=category_name)
        self.session.add(category)
        category_id, = self.session.query(Category.id).filter_by(name=category_name).first()
        item = Item(name=item_name, description=item_desc,
                    image_url=item_img, category_id=category_id, on_sale=False)
        self.session.add(item)
        item_id, = self.session.query(Item.id).filter_by(name=item_name, description=item_desc,
                                                         image_url=item_img, category_id=category_id,
                                                         on_sale=False).first()
        user = User(first_name=user_first_name, last_name=user_last_name, email=user_email, password_hash=user_password)
        self.session.add(user)
        user_id, = self.session.query(User.id).filter_by(first_name=user_first_name, last_name=user_last_name,
                                                         email=user_email, password_hash=user_password).first()
        self.session.commit()
        response = self.client.post('/favourite', json={
            'item_id': item_id,
            'user_id': user_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Favourite added successfully'})

        favourite_id, = self.session.query(Favourite.id).filter_by(item_id=item_id, user_id=user_id).first()

        response = self.client.delete(f'/favourite/{favourite_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Favourite deleted successfully'})

    def test_add_user(self):
        response = self.client.post('/user', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password_hash': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'User added successfully'})


if __name__ == '__main__':
    unittest.main()
