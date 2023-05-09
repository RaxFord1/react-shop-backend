DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE category (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE item (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  category_id INTEGER NOT NULL,
  on_sale BOOLEAN,
  FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  payment_method VARCHAR(20) NOT NULL,
  payment_amount DECIMAL(10,2) NOT NULL,
  payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE items_in_order (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders (id),
  FOREIGN KEY (item_id) REFERENCES items (id)
);

CREATE TABLE favourite (
  id INTEGER PRIMARY KEY,
  item_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (item_id) REFERENCES item (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);