from flask import render_template, Blueprint

blueprint = Blueprint('blueprint', __name__)

@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html', username='kennlebu')

@blueprint.route('/login')
def login():
    return render_template('login.html')

@blueprint.route('/signup')
def signup():
    return render_template('signup.html')
