from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activity.db'

from tracker import model
from tracker import controller

