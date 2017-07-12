from flask import render_template, Blueprint, session, request, flash, redirect, url_for
from .user import User

blueprint = Blueprint('blueprint', __name__)
users = []


@blueprint.route('/')
@blueprint.route('/index')
def index():
    """ The Bucket list home page showing a user's bucket list """

    # Take the user to the login page if they haven't logged in yet
    if not session.get('logged_in'):
        return redirect(url_for('blueprint.login'))

    return render_template('index.html', username=session['username'])

@blueprint.route('/login', methods=['GET','POST'])
def login():
    """ Logs in a user to DaBucketList """

    # Take the user to the index page if they are already logged in
    if session.get('logged_in'):
        return redirect(url_for('blueprint.index'))

    if request.method == 'POST':
        if request.form['login']:
            username = request.form['username']
            password = request.form['password']

            # If there are no users registered yet, redirect them to signup
            if len(users) < 1:
                flash('You need to signup to use DaBucketList', 'error')
                return redirect(url_for('blueprint.signup'))

            # One of more users have been found. Go ahead and check the credentials
            found = False
            for user in users:
                if user.username == username and user.password == password:
                    session['logged_in'] = True
                    session['username'] = username
                    found = True

            if not found:
                flash('Invalid username or password', 'error')
                return render_template('login.html', error='Error here')

            # Redirect to index page if the credentials are valid
            return redirect(url_for('index'))


    return render_template('login.html')

@blueprint.route('/signup', methods=['GET','POST'])
def signup():
    """ Signup a new user """

    # Take the user to the index page if they are already logged in
    if session.get('logged_in'):
        return render_template('login.html')

    if request.method == 'POST':
        # If submit has been clicked
        if session.get('signup'):
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            date_of_birth = request.form['dob']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if (not firstname and not lastname and not username and not date_of_birth
                and not password and not confirm_password):
                flash('All fields are required', 'error')
                return render_template('signup.html')
                
        

    return render_template('signup.html')

@blueprint.route('/logout')
def logout():
    """ Logs out a user """

    session['logged_in'] = False
    return render_template('login.html')
