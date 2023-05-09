import os

from flask import Flask

from config import config

from blueprints.db_api import dbAPI
from database.database import Base, engine

# Create the Flask app
app = Flask(__name__)
app.register_blueprint(dbAPI)


@app.route('/')
def home():
    return "Hello, world!" + "PSQL_URI: " + config.PSQL_URL


# @app.route('/init_db')
# def home():
#     Base.metadata.create_all(engine)
#     return "INITED DB "

Base.metadata.create_all(engine)
