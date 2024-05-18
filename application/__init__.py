from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask import url_for
# import config file:
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = "main.login_page"
login.login_message_category = "info"
from application import routes

def create_app(config=Config):
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  bcrypt.init_app(app)
  login.init_app(app)

  with app.app_context():
    from .routes import main
    app.register_blueprint(main)
  

  return app

