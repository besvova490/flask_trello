from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


from app import views
