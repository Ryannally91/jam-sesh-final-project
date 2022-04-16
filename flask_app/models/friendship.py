
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app

class Friendship:
    db =  'ijam_schema'
    def __init__(self, data):
        self.friend = data['friend'],
        self.user = data['user'],
        self.user_id = data['user_id'],
        self.friend_id = data['friend_id']


# create Friendship
    @classmethod
    def create_friendship(cls, data):
        #use hidden inputs from form to get ids
        query= '''
        Insert INTO friendships (user_id, friend_id)
        VALUES (%(user_id)s, %(friend_id)s)
        ;'''

        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def display_friendships(cls):
        query= '''
        SELECT users.first_name as user, users2.first_name as friend
        FROM users
        LEFT JOIN friendships ON users.id = friendships.user_id
        LEFT JOIN users as users2 ON users2.id = friendships.friend_id
        ;'''
# ____either query would work--------

        # query = ''' SELECT users.first_name as user, users2.first_name as friend, friendships.* FROM friendships
        # LEFT JOIN users ON users.id = friendships.user_id
        # Left Join users as users2 ON users2.id = friendships.friend_id;'''

        return connectToMySQL(cls.db).query_db(query)




