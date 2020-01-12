from flask import jsonify
from flask_login import login_required, logout_user, current_user, login_user
import flask, flask_login
import logging
from src.model import User
from src.repository import UserRepository, EventRepository
from werkzeug.security import generate_password_hash, check_password_hash
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

user_repo = UserRepository()
all_users = list(user_repo.get_all_users())

user = User('sragha45@example.com', 'password')
user_repo.add_user(user)

@login_manager.user_loader
def user_loader(email):
    logger.debug("User loader: " + email)
    if email not in (user.email for user in all_users):
        return

    for user in all_users:
        if user.email == email:
            return user

@login_manager.request_loader
def request_loader(request):
    logger.debug("Req : " + str(request))

    email = request['email']

    if email not in (user.email for user in all_users):
        return

    for user in all_users:
        if user.email == email:
            user.authenticated = request['password'] == user.password
            return user


@app.route('/login', methods=['POST'])
def login():
    req_json = flask.request.json
    email = req_json['email']
    for user in all_users:
        if user.email == email and user.password == req_json['password']:
            flask_login.login_user(user)

            return jsonify({'status': 'Logged in!'})
    return jsonify({'status': 'login failed'})


# TODO: Complete the implementation of REST API

app.run(debug=False)
