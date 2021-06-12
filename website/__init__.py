import os
path = os.path
environ = os.environ
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext
db = SQLAlchemy()
DB_NAME = 'database.db'
from .models import Task, User
from .views import views
from .auth import auth


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = r'{=RL<>3TDj;0{y)>l/&6Iy<>jHVd<{'
    uri = os.getenv("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['LANGUAGES'] = {'en': 'English', 'ru': 'Russian'}
    db.init_app(app)

    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = lazy_gettext('Please log in to access this page.')
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    return app

def create_database(app):
    db.create_all(app=app)