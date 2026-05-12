from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# DB + Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'   # where to redirect if not logged in


login_manager.login_message = "Please log in to continue."

# Import routes and models
from app import routes, models