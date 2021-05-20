from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = 'database.db'
from .models import Task, User
from .views import views
from .auth import auth


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = r'{=RL<>3TDj;0{y)>l/&6Iy<>jHVd<{'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created database!")