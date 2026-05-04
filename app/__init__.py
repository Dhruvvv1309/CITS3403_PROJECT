from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config) #loads the configuration from the Config class in config.py
db = SQLAlchemy(app) #creates the database object
migrate = Migrate(app, db)

from app import routes, models

