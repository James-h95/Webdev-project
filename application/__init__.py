from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hangman.db'
app.config['SECRET_KEY'] = '290429d88cc03bbf9526fc4e'
db = SQLAlchemy(app)


from application import routes
