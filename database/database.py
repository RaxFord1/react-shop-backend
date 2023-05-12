import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from config.config import PSQL_URL

# Set up the database connection
PSQL_URI = PSQL_URL
print("PSQL_URI: ", PSQL_URI)
engine = create_engine(PSQL_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Define the Category model
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)  # label
    value = Column(String, nullable=False, unique=True)  # value


# Define the Item model
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='items')
    on_sale = Column(Boolean)
    price = Column(Float, nullable=False)


# Define the User model
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String)
    admin = Column(Boolean, default=False)


# Define the Order model
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='orders')
    order_date = Column(DateTime, default=datetime.utcnow)
    paid = Column(Boolean, default=False)


# Define the OrderItem model
class OrderItem(Base):
    __tablename__ = 'order_items'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True, nullable=False)


# Define the Favourite model
class Favourite(Base):  # uk - Favourite | US - Favorite
    __tablename__ = 'favourite'
    id = Column(Integer, primary_key=True, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship('Item')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')

    __table_args__ = (
        UniqueConstraint('item_id', 'user_id', name='uq_favourite_item_user'),
    )


if __name__ == "__main__":
    # Create the tables in the database
    Base.metadata.create_all(engine)
