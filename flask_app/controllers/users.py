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
    return redirect(f'/dashboard/{this_user.id}')


@app.route('/registration')
def registration_form():
    return render_template('registration.html', states = states)

@app.route('/register/user', methods=['POST'])
def register():
    user_id = user.User.register_user(request.form)
    if user_id:
        return redirect (f"/dashboard/{session['user_id']}")
    return redirect ('/')

@app.route('/dashboard/<int:id>')
def home(id):

    return render_template('dashboard.html',  events = event.Event.get_all_events())

@app.route('/user/profile/<int:id>')
def user_profile(id):
    _user = user.User.get_user_by_id(id)
    return render_template('show_profile.html', user = _user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# @app.route('/show_info', methods=["POST"])
# def display():
#     if not user.User.validate_submission(request.form):
#         return redirect('/')
#     session['name'] = request.form["name"]
#     session['location'] = request.form["location"]
#     session['language'] = request.form['language']
#     session['comments'] = request.form['comments']
#     users.append(session)
#     return redirect ('/information') 

# @app.route('/information')
# def show():
#     return render_template('display.html')

# @app.route('/newsubmit')
# def reset():
#     session.clear()
#     return redirect('/')