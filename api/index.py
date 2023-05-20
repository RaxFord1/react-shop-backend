from flask import Flask
from flask_cors import CORS

from blueprints.auth_api import authAPI
from config import config

from blueprints.db_api import dbAPI
from database.database import Base, engine

# Create the Flask app
app = Flask(__name__)
CORS(app)
app.register_blueprint(dbAPI)
app.register_blueprint(authAPI)


@app.route('/')
def home():
    return "Hello, world!" + "PSQL_URI: " + config.PSQL_URL


# @app.route('/init_db')
# def home():
#     Base.metadata.create_all(engine)
#     return "INITED DB "

Base.metadata.create_all(engine)
app.run()
