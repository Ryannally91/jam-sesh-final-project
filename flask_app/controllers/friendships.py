from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user, friendship 
from flask_app.controllers import users


@app.route('/create_friendship', methods=['POST'])
def make_friendship():
    friendship.Friendship.create_friendship(request.form)
    return redirect('/friendships')