from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__, template_folder="views")
    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
