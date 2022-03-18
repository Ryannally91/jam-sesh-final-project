from dataclasses import dataclass
from datetime import datetime, date
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for, jsonify
from flask_app.models import user, message, comment, event
from flask_app.controllers import users, comments
import requests #have to install for api requests to gmap
from google_api_key import api_key
from urllib.parse import urlencode
import json


states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

@app.route('/search_event')
def search_event():
    
    return render_template('search_event.html')



@app.route('/search_results', methods=['POST'] )
def search_results():
    print(request.form)
    if request.form['location'] !='' and request.form['date'] !='':
        new_location = request.form['location'].split(', ')
        data = {
            'city' : new_location[-3],
            'state': new_location[-2],
            'date' : request.form['date']
        }
        events = event.Event.get_events_by_city_date_ajax(data)
    elif request.form['date'] !='':
        events= event.Event.get_events_by_date(request.form)
    
    else:
        new_location = request.form['location'].split(', ')
        data = {
            'city' : new_location[-3],
            'state': new_location[-2]
        }
        events= event.Event.get_events_by_city_ajax(data)
    #return by location only
    for _event in events:
        print(_event,  ' ##################################')
    return jsonify(events)
    #display as AJAX with pagination

@app.route('/search_by_user_loc', methods=["POST"])
def search_by_user_loc():
    data = {
        'city' : session['user_city'],
        'state' : session['user_state']
    }
    events = event.Event.get_events_by_city_ajax(data)
    return jsonify(events)

@app.route('/create_event_form')
def create_event_form():
    if 'user_id' not in session:
        return render_template('index.html')
    return render_template('create_event.html', states = states, current_day = str(date.today()))

@app.route('/create_event', methods= ['POST'])
def create_event():
    if 'user_id' not in session:
        return render_template('index.html')
    if not event.Event.validate_event(request.form):
        return redirect('/create_event_form') 
    session['event_id'] = event.Event.create_event(request.form)
    return redirect(f"/success/{session['event_id']}") 
   

@app.route('/success/<int:id>')
def success(id):
    _event = event.Event.get_event_by_id(id)
    return render_template('success.html', event = _event)

@app.route('/event_details/<int:id>')
def show(id):
    if 'user_id' not in session:
        return render_template('index.html')
    this_event = event.Event.get_event_by_id(id)
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    location = this_event.location
    print(location)
    params = {
    "key": api_key,
    "input": {location},
    "inputtype": "textquery",
    "fields": "place_id,formatted_address,name,geometry"
    }

    params_encoded = urlencode(params)
    places_endpoint = f"{base_url}?{params_encoded}"

    r = requests.get(places_endpoint)
    #if len(r.candidates) <1:  redirect with flash errors
    # put this as validation when creating an event (put in create controler, use form data to pass through)
    print(r.status_code)
    print(r.json())  
    r = r.json()
    
    return render_template('show_event.html', event = this_event, r = r )

@app.route('/edit/event/<int:id>')
def edit_event_form(id):
    if 'user_id' not in session:
        return render_template('index.html')
    _event = event.Event.get_event_by_id(id)
    print(_event.state,'----', _event.location, _event.city)
    return render_template('edit_event_form.html', event = _event)

@app.route('/update_event/<int:id>', methods = ['POST'])
def update_event(id):
    print('++++++++++++++', request.form,'+++++++++++++')
    if not event.Event.validate_event(request.form):
            return redirect(f'/edit/event/{id}') 
    print(request.form['id'], '$$$$$$$$$$$$$$$$44')
    data = event.Event.parse_location(request.form)
    data['id'] =id
    event.Event.update_event_by_id(data)
    return redirect(f'/success_update/{id}')

@app.route('/success_update/<int:id>')
def success_update(id):
    _event = event.Event.get_event_by_id(id)
    return render_template('success_update.html', event = _event)
    
@app.route('/delete/event/<int:id>')
def delete_event(id):
    if 'user_id' not in session:
        return render_template('index.html')
    event.Event.delete_event(id)
    return redirect (f"/dashboard/{session['user_id']}")



# , results = event.Event.get_events_by_city(request.form)

@app.route('/RSVP/<int:id>', methods = ['POST'])
def rsvp(id):
    event.Event.rsvp(request.form)
    return redirect(f'/success/{id}')
