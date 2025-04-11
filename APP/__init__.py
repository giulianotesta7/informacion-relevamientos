from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()

from flask import Flask
from .views import views
from .auth import auth
from os import path
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] =(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    ) 
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    db.init_app(app)
    migrate = Migrate(app, db)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Relevamientos

    
    Login_manager = LoginManager()
    Login_manager.login_view = 'auth.login'
    Login_manager.init_app(app)

    @Login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.context_processor
    def inject_tinymce_key():
        return {'TINYMCE_API_KEY': os.getenv('TINYMCE_API_KEY')}

    return app

