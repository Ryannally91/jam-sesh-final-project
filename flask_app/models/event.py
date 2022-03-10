from datetime import datetime, date
from time import strftime, gmtime
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
import re	# the regex module
from flask_bcrypt import Bcrypt   
from flask_app.models import message, event, friendship, user  


class Event:
    db ='ijam_schema'
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.location = data['location']
        self.state = data['state']
        self.city = data['city']
        self.user_id = data['user_id']
        self.date = data['date'] 
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.host = user.User.get_user_by_id(data['user_id'])  #or use query
        self.rsvp = [] # may need to be its own table.  Many to many  Users can have many events, events have many users attending


        ###  Instance method for date display

#CREATE
    @classmethod
    def create_event(cls, data):
        if not cls.validate_event(data):
            return False
        data = cls.parsed_data(data)
        query='''
        INSERT INTO events (event_name, location, state, city, user_id, date, start_time, end_time, description)
        VALUES (%(event_name)s, %(location)s, %(state)s, %(city)s, %(user_id)s, %(date)s, %(start_time)s, %(end_time)s, %(description)s);''' # will need hidden input with recipient id when sending message
        return connectToMySQL(cls.db).query_db(query,data)


#Read

    @classmethod
    def get_all_events(cls): 
        query = """
        SELECT events.*, users.first_name, users.last_name
        FROM events
        LEFT JOIN users ON users.id = events.user_id
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        events = []
        for row in result:
            events.append(cls(row))
        return events
        # to use query to get host might need to create dict then pass into user class


    @classmethod
    def get_event_by_id(cls, id):
        data = {'id' : id}
        query = '''SELECT * FROM events
                WHERE id = %(id)s
                ;'''
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def get_events_by_user_id(cls, id):
        pass
    ##find jams near user location

    @classmethod
    def get_events_by_date(cls, data):
        query = '''SELECT * FROM events
                    WHERE date = %(date)s
                ;'''
        result = connectToMySQL(cls.db).query_db(query,data)
        # events = []
        for i in range(len(result)): 
            result[i]['start_time'] = str(result[i]['start_time'])
            result[i]['end_time'] = strftime("%H:%M", gmtime(result[i]['end_time']))
        return result
        # from request.form(start and end) plug those values in display in templates table
        # WHERE date_time >= %(date_time_start)s AND date_time <= %(date_time_end)s

    @classmethod
    def get_events_by_city(cls, data):
        query = '''SELECT * FROM events
                WHERE city = session['user_city']  AND state = session['user_state']
                ;'''   ###May need to revise query
        result = connectToMySQL(cls.db).query_db(query,data)
        events = []
        for row in result: 
            events.append(cls(row))
        return events
    @classmethod
    def add_user_to_event():
        pass


    #UPDATE

    @classmethod
    def update_event_by_id(cls, data):
        query = """
        UPDATE events
        SET event_name = %(event_name)s, location = %(location)s,  state = %(state)s,  city = %(city)s, date_time = %(date_time)s, description = %(description)s, user_id= %(user_id)s
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    
    #DELETE
    @classmethod
    def delete_event(cls,id):
        data = { 'id' : id }
        query = """
        DELETE * FROM events
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)



########### VALIDATE EVENT !!!!!!!!!!!!!!!!!
    @staticmethod
    def validate_event(data):
        is_valid = True # assume true
        if len(data['event_name']) < 5:
            flash('Name must be 5 or more characters', 'event')
            is_valid = False
        if len(data['location']) < 1:
            flash('Location cannot be blank', 'event')
            is_valid = False
        if data['date'] == '': #not boolean, must compre to empty string to validate  # Need to compare to present date, anything prior is invalid
            flash('must enter date', 'event') 
            is_valid = False
        #Check to see if date is in future
        if data['date'] < str(date.today()):
            flash('date must be later than today')
            is_valid = False
        if data['start_time'] =='' or data['end_time'] =='':
            flash('must enter both start and end time', 'event') 
            is_valid = False
        #check to see that start and end are sequential  start < end
        if data['start_time'] > data['end_time']:
            flash('Start time cannot be late than end time', 'event') 
            is_valid = False
        if len(data['description']) < 10 or len(data['description']) > 300:
            flash('description must be between ten or 300 characters', 'event')
            is_valid = False
        if len(data['city']) < 1 or len(data['city']) > 45 or not data['city'].isalpha():
            flash('city must be between 1 and 45 letters')
            is_valid = False
        return is_valid


    @staticmethod
    def parsed_data(data):
        parsed_data={
            'event_name': data['event_name'],
            'location': data['location'],
            'city': data['city'].lower().strip(),
            'state': data['state'],
            'user_id': data['user_id'],
            'date' : data['date'],
            'start_time' : data['start_time'],
            'end_time' : data['end_time'],
            'description': data['description']
        }
        return parsed_data
