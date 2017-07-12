from flask import Flask
from .views import blueprint

app = Flask(__name__)

app.register_blueprint(blueprint)
#app.config.from_object('config')
app.static_folder = 'assets'
app.config["DEBUG"] = True
