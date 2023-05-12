from flask import jsonify, request, Blueprint
from werkzeug.exceptions import Unauthorized

from database.database import Session, User

authAPI = Blueprint('auth_api', __name__, template_folder='templates')


@authAPI.route('/login', methods=['POST'])
def login():
    # TODO: может всё таки jwt?
    session = Session()
    email = request.json.get('email')
    password = request.json.get('password')
    user_result = session.query(User.id).filter_by(email=email, password_hash=password).first()
    session.close()

    if user_result is None:
        return Unauthorized()

    return jsonify({'id': user_result[0]})
