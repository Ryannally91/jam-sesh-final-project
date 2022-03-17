from datetime import datetime, date
from time import gmtime, strftime
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from flask_app import app
import re	# the regex module
from flask_bcrypt import Bcrypt   
from flask_app.models import message, friendship, user  


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
        self.rsvp_list = [] # may need to be its own table.  Many to many  Users can have many events, events have many users attending



#CREATE
    @classmethod
    def create_event(cls, data):
        data = cls.parse_location(data)
        query='''
        INSERT INTO events (event_name, location, state, city, user_id, date, start_time, end_time, description)
        VALUES (%(event_name)s, %(location)s, %(state)s, %(city)s, %(user_id)s, %(date)s, %(start_time)s, %(end_time)s, %(description)s);''' # will need hidden input with recipient id when sending message
        
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def rsvp(cls, data):
        query='''
        INSERT INTO RSVP (user_id, event_id)
        VALUES (%(user_id)s, %(event_id)s);'''
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
        # print(">>>>>>>>>>",result)
        events = []
        for row in result:
            # row['start_time'].strftime("%I:%M %p")
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
        # print(results)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def get_events_by_user_id(cls,id):
        data = {'user_id' : id}
        query = '''SELECT * FROM events
                WHERE user_id = %(user_id)s
                ;'''   ###May need to revise query
        result = connectToMySQL(cls.db).query_db(query,data)
        events = []
        for row in result: 
            # row['start_time'].strftime("%I:%M %p")
            events.append(cls(row))
        # print(events)
        return events
    ##find jams near user location

    @classmethod
    def get_events_by_date(cls, data):
        query = '''SELECT * FROM events
                    WHERE date = %(date)s
                ;'''
        result = connectToMySQL(cls.db).query_db(query,data)
        # print(result)
        # events = []
        for i in range(len(result)):  
            result[i]['start_time'] = 'test'
            result[i]['end_time'] = 'test'
        return result
        

    @classmethod
    def get_events_by_city_ajax(cls, data):
        query = '''SELECT * FROM events
                WHERE city = %(city)s  AND state = %(state)s
                ;'''   ###May need to revise query
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        for i in range(len(result)): 
            # print(result[i]['start_time'])
            # print( gmtime(result[i]['start_time']) ) 
            result[i]['start_time'] = 'test'
            result[i]['end_time'] = 'test'
            # print(result[i]['start_time'],
            # result[i]['end_time'])
        return result

    @classmethod
    def get_events_by_city_date_ajax(cls, data):
        query = '''SELECT * FROM events
                WHERE city = %(city)s 
                AND state = %(state)s 
                AND date = %(date)s
                ;'''   ###May need to revise query
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        for i in range(len(result)): 
            result[i]['start_time'] = 'test'
            result[i]['end_time'] = 'test'
        return result

    @classmethod
    def get_events_by_city(cls, data):
        query = '''SELECT * FROM events
                WHERE city = %(city)s  AND state = %(state)s
                ;'''   ###May need to revise query
        result = connectToMySQL(cls.db).query_db(query,data)
        events = []
        for row in result: 
            events.append(cls(row))
        return events
    
    #UPDATE

    @classmethod
    def update_event_by_id(cls, data):
        # id_event = data['id']
        # data = cls.parse_location(data)
        # data['id'] = id_event
        query = """
        UPDATE events
        SET event_name = %(event_name)s, location = %(location)s,  state = %(state)s,  city = %(city)s, date = %(date)s, description = %(description)s, start_time = %(start_time)s, end_time= %(end_time)s
        WHERE events.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    
    #DELETE
    @classmethod
    def delete_event(cls,id):
        data = { 'id' : id }
        print('-------------madeit', data)
        query = """
        DELETE FROM events
        WHERE id = %(id)s
        ;""" # * in delete query
        return connectToMySQL(cls.db).query_db(query, data)



########### VALIDATE EVENT !!!!!!!!!!!!!!!!!
    @classmethod
    def validate_event(cls, data):
        data = cls.parse_location(data) #could make as cls method and put here one time instead of contollers multiple times
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
    def parse_location(data):
        location_breakdown = data['location'].split(',')
        print(location_breakdown)
        location = ', '.join([str(item) for item in location_breakdown[:-3]])
        parsed_data = {
            'location' : location,
            'city' : location_breakdown[-3].strip(),
            'state' : location_breakdown[-2].strip(),
            'event_name': data['event_name'],
            'user_id': data['user_id'],
            'date' : data['date'],
            'start_time' : data['start_time'],
            'end_time' : data['end_time'],
            'description': data['description']
        }
        print(data)
        return parsed_data

