from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user, message, event
from flask_app.controllers import messages, comments, events
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect(f"dashboard/{session['user_id']}")

@app.route('/login', methods=['POST'])
def sign_in():
    data = {
        "email": request.form['email'],
        "password" : request.form['password']
    }
    if not user.User.login(data):
        return redirect('/')
    this_user = user.User.find_by_email(data)
    session['user_id'] = this_user.id
    session['first_name'] = this_user.first_name
    session['user_city'] =this_user.user_city
    session['user_state'] = this_user.user_state
    return redirect(f'/dashboard/{this_user.id}')
    
@app.route('/registration')
def registration_form():
    return render_template('registration.html', states = states)

@app.route('/register/user', methods=['POST'])
def register():
    user_id = user.User.register_user(request.form)
    if user_id:
        return redirect (f"/dashboard/{session['user_id']}")
    return redirect ('/registration')

@app.route('/dashboard/<int:id>')
def home(id):
    hosted_events = event.Event.get_events_by_user_id(id)
    data = {
        'city' : session['user_city'],
        'state' : session['user_state'],
    }
    _events = event.Event.get_events_by_city(data)
    return render_template('dashboard.html',  events = _events, hosted_events = hosted_events)

@app.route('/user/profile/<int:id>')
def user_profile(id):
    _user = user.User.get_user_by_id(id)
    return render_template('show_profile.html', user = _user)


@app.route('/update/user/<int:id>', methods = ['POST'])
def update_user(id):
    if 'user_id' not in session:
        return redirect ('/')
    if not user.User.validate_update(request.form):
        return redirect(f'/edit_account_settings/{id}')
    data = request.form
    # data['id'] = id
    print(data)
    user.User.update_user(data)
    return redirect('/')

@app.route('/edit_account_settings/<int:id>')
def edit_user_form(id):
    if 'user_id' not in session:
        return render_template('index.html')
    this_user = user.User.get_user_by_id(id)
    return render_template('edit_account_settings.html', user = this_user, states = states)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

