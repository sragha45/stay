from flask_login import login_required, logout_user, current_user, login_user
import flask, flask_login

from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(email):
    users =

def login():

