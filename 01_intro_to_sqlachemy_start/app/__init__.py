from flask import Flask
from config import Config # ADDED
from flask_sqlalchemy import SQLAlchemy # ADDED
from flask_migrate import Migrate # ADDED

app = Flask(__name__)
app.config.from_object(Config) #ADDED
db = SQLAlchemy(app) #ADDED
migrate = Migrate(app, db) #ADDED

from app import routes, models # MODIFIED