from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app import app
import re, math
from datetime import datetime
from flask_app.models import user



class Message:
    db = 'ijam_schema'
    def __init__(self, data): 
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.sender = user.User.get_user_by_id(data['sender_id'])
        self.recipient_id = data['recipient_id']
        self.recipient = user.User.get_user_by_id(data['recipient_id'])
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    def timestamp(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    #CREATE
    @classmethod
    def create_message(cls, data):
        
        query='''
        INSERT INTO messages (content, sender_id, recipient_id)
        VALUES (%(content)s,%(sender_id)s,%(recipient_id)s);''' # will need hidden input with recipient id when sending message
        print('made it this far <<><><><')
        return connectToMySQL(cls.db).query_db(query,data)

    #READ
    @classmethod
    def get_all_messages_by_user_id(cls, id):
        data= {'id' : id}
        query='''SELECT users.first_name as recipient, users2.first_name as sender, messages.*
        FROM messages
        LEFT JOIN users ON users.id = messages.recipient_id
        LEFT JOIN users as users2 ON users2.id = messages.sender_id 
        WHERE users.id = %(id)s;'''  

        result= connectToMySQL(cls.db).query_db(query, data)
        if result:
            messages=[]
            for m in result:
                messages.append(cls(m))
            return messages
        return result
           

    @classmethod
    def delete_message(cls, id):
        data ={ "id" : id}
        query= '''
        DELETE FROM messages
        WHERE id = %(id)s
        ;'''
        print('made ','it')
        return connectToMySQL(cls.db).query_db(query, data)