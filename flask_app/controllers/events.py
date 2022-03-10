from dataclasses import dataclass
from datetime import datetime, date
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for, jsonify
from flask_app.models import user, message, comment, event
from flask_app.controllers import users, comments
import requests #have to install for api requests to gmap

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

@app.route('/search_event')
def search_event():
    # events = event.Event.get_events_by_city()
    return render_template('search_event.html', states= states)

@app.route('/search_results', methods=['POST'] )
def search_results():
    # if request.form['city'] and request.form['date']:
    # if request.form['date']:
    events= event.Event.get_events_by_date(request.form)
    for _event in events:
        print(_event)
    return jsonify(events)
    #display as AJAX with pagination

@app.route('/create_event_form')
def create_event_form():
    return render_template('create_event.html', states = states, current_day = str(date.today()))

@app.route('/create_event', methods= ['POST'])
def create_event():
    if event.Event.create_event(request.form):
        return redirect('/success')
    return redirect('/create_event_form') 

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/event_details/<int:id>')
def show(id):
    this_event = event.Event.get_event_by_id(id)
    print(this_event)
    return render_template('show_event.html', event = this_event )



# , results = event.Event.get_events_by_city(request.form)