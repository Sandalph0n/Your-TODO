from flask import Flask, redirect, render_template, url_for, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



db = SQLAlchemy()
DATABASE_NAME = "todo.db"

def create_app():
    from .views import views
    from .auth import auth
    from .models import User, Task

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'THIS IS REALLY SECRET'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
    db.init_app(app)


    app.register_blueprint(views, url_prefix= "/")
    app.register_blueprint(auth, url_prefix= "/")

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.sign_in"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # create_database()
    
    return app
    
def create_database():
    if not path.exists('website/instance/' + DATABASE_NAME):
        db.create_all()
        print('Created Database!')