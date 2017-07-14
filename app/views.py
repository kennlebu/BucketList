from flask import render_template, Blueprint, session, request, flash, redirect, url_for
from .user import User
import sys

blueprint = Blueprint('blueprint', __name__)
users = []


@blueprint.route('/')
@blueprint.route('/index')
def index(category=None):
    """ The Bucket list home page showing a user's bucket list """

    # Take the user to the login page if they haven't logged in yet
    if not session.get('logged_in'):
        return redirect(url_for('blueprint.login'))

    # Pass the signed in user to the template
    logged_in_user = get_loggedin_user()

    # Check whether user has bucket lists
    has_bucketlists = False
    if len(logged_in_user.bucketlists) > 0:
        has_bucketlists = True

    return render_template('index.html', name=session['name'],
                           user=logged_in_user, has_bucketlists=has_bucketlists)

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
                    session['name'] = user.firstname + ' ' + user.lastname
                    session['username'] = username
                    found = True

            if not found:
                return render_template('login.html', error='Invalid username or password')

            # Redirect to index page if the credentials are valid
            return redirect(url_for('blueprint.index'))


    return render_template('login.html')

@blueprint.route('/signup', methods=['GET','POST'])
def signup():
    """ Signup a new user """

    # Take the user to the index page if they are already logged in
    if session.get('logged_in'):
        return render_template('login.html')

    if request.method == 'POST':

        # If submit has been clicked
        if request.form['signup']:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            date_of_birth = request.form['dob']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if (not firstname or not lastname or not username or not date_of_birth
                    or not password or not confirm_password):
                return render_template('signup.html', error='All fields are required')

            # Check if passwords match
            if not password == confirm_password:
                return render_template('signup.html', error='The passwords should match')

            # Check whether username is already taken
            for user in users:
                if username == user.username:
                    return render_template('signup.html', error="That username is already taken")

            # Create the user
            new_user = User(username, password, firstname, lastname, date_of_birth)
            users.append(new_user)

            # Redirect to login
            return redirect(url_for('blueprint.login'))

    return render_template('signup.html')

@blueprint.route('/logout')
def logout():
    """ Logs out a user """

    session['logged_in'] = False
    return redirect(url_for('blueprint.login'))

@blueprint.route('/item', methods=['GET','POST'])
def view_item():
    """ Views, edits or adds a new bucketlist item """

    # Check whether adding a new bucketlist or editing or viewing one
    request_type = request.args.get('type')
    if request_type == 'new':
        return render_template('bucket-list-item.html', request_type=request_type)
    elif request_type == 'view':
        logged_in_user = get_loggedin_user()
        bucketlist = get_bucketlist(logged_in_user, request.args.get('bucketlist'))

        return render_template('bucket-list-item.html', request_type=request_type,
                               bucketlist_name=bucketlist.name,
                               due_date=bucketlist.due_date,
                               bucketlist_items=bucketlist.items,
                               name=session['name'])

    return render_template('bucket-list-item.html', name=session['name'])

@blueprint.route('/add_bucketlist', methods=['GET', 'POST'])
def add_bucketlist():
    """ Adds a new bucket list. Also edits a bucketlist if one is specified using a post request """

    if request.method == 'POST':

        # If submit has been clicked
        if request.form['add_bucketlist']:
            bucketlist_name = request.form['bucketlist_name']
            due_date = request.form['due_date']
            request_type = request.form['request_type']

            # Check if its a new bucketlist or just an edit
            if request_type == 'new':
                # Get the logged in user
                logged_in_user = get_loggedin_user()

                if logged_in_user:
                    logged_in_user.create_bucketlist(bucketlist_name, due_date)

                return redirect(url_for('blueprint.index'))

            # If the user is editing an existing bucketlist
            elif  request_type == 'edit':
                # Get the logged in user
                logged_in_user = get_loggedin_user()

                if logged_in_user:
                    # Get the created bucketlist and edit the items
                    bucketlist = get_bucketlist(logged_in_user, request.form['old_name'])

                    bucketlist.name = bucketlist_name
                    bucketlist.due_date = due_date

                    return redirect(url_for('blueprint.index'))


    return redirect(url_for('blueprint.index'))

@blueprint.route('/markitem', methods=['GET', 'POST'])
def mark_item():
    """ Marks a bucket list item as done (accomplished) or undone """

    if request.method == 'POST':
        if request.form['checked']:
            # Get the user we want
            our_user = None
            for person in users:
                if person.username == session['username']:
                    our_user = person

            # If the item has been checked, mark it as done
            if request.form['checked'] == 'checked':
                # Get the bucket list item and mark it as done
                for bucketlist in our_user.bucketlists:
                    if bucketlist.name == request.form['bucketlist_name']:
                        bucketlist.mark_item_as_done(request.form['item_name'])
                        return "marked as done"
                    return "bucketlist not found"

            elif request.form['checked'] == 'not_checked':
                # Get the bucket list item and mark it as undone
                for bucketlist in our_user.bucketlists:
                    if bucketlist.name == request.form['bucketlist_name']:
                        bucketlist.mark_item_as_undone(request.form['item_name'])
                        return "marked as undone"
                    return "bucketlist not found"

            else:
                return "not checked or checked. Just weird"

        return "Checked value not passed"


    return "Just a return"

@blueprint.route('/delete_bucketlist', methods=['GET', 'POST'])
def delete_bucketlist():
    """ Deletes a bucketlist """

    bucketlist_name = request.args.get('bucketlist_name')
    user = get_loggedin_user()
    bucketlist = get_bucketlist(user, bucketlist_name)

    # Remove the bucketlist from the user's list of bucketlists
    user.bucketlists.remove(bucketlist)
    return render_template('index.html')

@blueprint.route('/edit_bucketlist', methods=['GET', "POST"])
def edit_bucketlist():
    """ Edits a bucketlist """

    bucketlist_name = request.args.get('bucketlist_name')
    user = get_loggedin_user()
    bucketlist = get_bucketlist(user, bucketlist_name)

    # Return the values in the bucketlist to the page for editing
    return render_template('bucket-list-item.html', bucketlist=bucketlist, request_type='edit')

@blueprint.route('/add-item', methods=['GET', 'POST'])
def add_item():
    """ Adds an item to a bucketlist """

    if request.method == 'POST':
        if request.form['add_item']:

            # If the item name is not empty
            if request.form['item_name']:
                user = get_loggedin_user()
                bucketlist = get_bucketlist(user, request.form['bucketlist_name'])

                # Add the item to the bucketlist
                bucketlist.add_item(request.form['item_name'])

                return render_template('bucket-list-item.html', request_type='view',
                                       bucketlist_name=bucketlist.name,
                                       due_date=bucketlist.due_date,
                                       bucketlist_items=bucketlist.items,
                                       name=session['name'])

def get_loggedin_user():
    """ Returuns the user that is logged in """

    for person in users:
        if person.username == session['username']:
            return person

def get_bucketlist(user, bucketlist_name):
    """ Returns the bucketlists of the logged in user """

    for bucket in user.bucketlists:
        if bucket.name == bucketlist_name:
            return bucket
