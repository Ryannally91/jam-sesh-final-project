from dataclasses import dataclass
from email import message
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user, message, event
from flask_app.controllers import users



@app.route('/create_message', methods = ['POST'])
def send_message():
    print("I made it this far!!!!!")
    
    message.Message.create_message(request.form)
    return redirect (f"/dashboard/{session['user_id']}")

@app.route('/inbox/<int:id>')
def inbox(id):
    return render_template('inbox.html', messages = message.Message.get_all_messages_by_user_id(id))

@app.route('/delete/<id>')
def delete(id):
    message.Message.delete_message(id)
    return redirect (f"/dashboard/{session['user_id']}")