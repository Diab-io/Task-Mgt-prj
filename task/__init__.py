from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

DB_NAME = 'database.db'
db = SQLAlchemy()

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    from .views import view
    from .auth import auths

    from .models import User, Todo

    create_database(app)
    
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')

    return app

def create_database(app):
    if not os.path.exists('task/instance' + DB_NAME):
        with app.app_context():
            db.create_all()