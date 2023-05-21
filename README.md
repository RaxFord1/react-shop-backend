# React-Shop Backend
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/RaxFord1/react-shop-backend/blob/master/LICENSE.md)

This repository contains the server-side component of the React-Shop e-commerce web application. It handles all data operations, user authentication, and other server-side tasks necessary for smooth operation of the application.

## Table of Contents
1. [About the Project](#about-the-project)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Frontend Code](#frontend-code)
7. [License](#license)

## About the Project
The React-Shop Backend is a robust and scalable backend solution for e-commerce applications. It is designed to handle a variety of tasks such as user authentication, product categorization, order management, and user feedback, making it a comprehensive backend solution for online retail platforms.

## Tech Stack
This project uses the following key technologies:
- Python
- Flask
- SQLAlchemy
- PostgreSQL

## Project Structure
Here's a snapshot of the project's file structure:
- `api/index.py` - Main file and entry point for the backend.
- `blueprints/` - Contains endpoint blueprints for authorization (`auth_api.py`) and database operations (`db_api.py`).
- `database/` - Includes files for database table creation (`database.py`) and database initialization (`init.py`).
- `config/config.py` - Configuration file specifying the path to the database.
- `tests/simple_database_api_tests.py` - Contains tests for the database API.

## Database Schema
The PostgreSQL database used by React-Shop Backend follows this structure:
- `Category` (id, name, value)
- `Item` (id, name, description, image_url, category_id, on_sale, price)
- `User` (id, first_name, last_name, email, password_hash)
- `Order` (id, user_id, order_date, paid)
- `OrderItem` (order_id, item_id)
- `Favourite` (id, item_id, user_id)
- `Review` (id, text, item_id, user_id)
- 
![React-Shop Frontend](https://github.com/RaxFord1/react-shop-backend/blob/main/public/physical-model-database.jpg?raw=true)


## API Endpoints
The backend provides a variety of endpoints for handling different operations:
- `/login`: POST request to authenticate a user login.
- `/categories`: GET request to retrieve all categories.
- `/category`: POST request to add a new category.
- `/category/<int:category_id>`: DELETE request to remove a category using its ID.
- `/items`: GET request to fetch all items.
- `/item`: POST request to add a new item.
- `/item/<int:item_id>`: PUT request to update an item by ID.
- `/item/<int:item_id>`: DELETE request to remove an item by ID.
- `/favourite`: POST request to add an item to the user's favorites.
- `/favourite/<int:user_id>/<int:item_id>`: DELETE request to remove an item from the user's favorites.
- `/favourite/<int:user_id>`: GET request to retrieve a user's favorite items.
- `/user`: POST request to register a new user.
- `/order`: POST request to create a new order.
- `/last_unpaid_order/<int:user_id>`: GET request to retrieve the last unpaid order of a user.
- `/order_item`: POST request to add an item to an order.
- `/order_items/<int:order_id>`: GET request to retrieve all items in an order.
- `/pay`: POST request to mark an order as paid.
- `/order_item/<int:order_id>/<int:item_id>`: DELETE request to remove an item from an order.
- `/review`: POST request to create a new review for an item.
- `/review/<int:item_id>`: GET request to retrieve all reviews for a specific item.
Please feel free to explore these endpoints to better understand the functionality provided by the React-Shop Backend.

## Frontend Code
The frontend code for the React-Shop application can be found [here](https://github.com/RaxFord1/react-shop).

![React-Shop Frontend](https://github.com/RaxFord1/react-shop/blob/master/public/screenshot.png?raw=true)

## License
This project is licensed under the terms of the license provided in the repository. Please see the LICENSE file for details.

## Conclusion
I hope you find this backend service useful for your e-commerce application. If you have any questions or encounter any issues, please feel free to open an issue or make a pull request.
