from flask import Flask
from .views import blueprint
import os

app = Flask(__name__)

app.register_blueprint(blueprint)

app.static_folder = 'assets'
app.secret_key = os.urandom(12)
app.config["DEBUG"] = True
