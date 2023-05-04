from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from .views import view
    from .auth import auths
    
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auths, url_prefix='/')

    return app