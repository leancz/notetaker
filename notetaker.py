# -*- coding: utf-8 -*-
"""
Funky lil note taker or chatter
"""

from flask import Flask, session, redirect, url_for, escape, request
import json
import os
import datetime

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
database = 'd:\\tmp\\my_db.json'

def read_db():
    if os.path.isfile(database):
        with open(database) as f:
            json_data = json.load(f)
    else: json_data = [('2001-01-01 12:00:00', 'guest', 'Welcome')]
    return json_data
    
def write_db(comment):
    # read whole db
    json_data = read_db()
    # add comment
    json_data.append(comment)
    # write whole db
    with open(database, 'w') as f:
        json.dump(json_data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if logged_in():
        if request.method == 'POST':
            # store request.form['comment'] in database
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_db((ts, session['username'],request.form['comment']))
            return redirect(url_for('index'))
        records = read_db()
        output = '''
        <form method="post">
            <p><textarea name=comment rows="10" cols="80"></textarea>
            <p><input type=submit value=AddComment>
        </form>
        '''
        for record in records:
            output = output + '<p>' + record[0] + ' (' + record[1] + ')'
            output = output + '<br />' + record[2] + '</p>'
        return output
    return 'You are not logged in'
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def logged_in():
    if 'username' in session: return True
    return False
    
@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        # store request.form['comment'] in database
        write_db(request.form['comment'])
        return redirect(url_for('index'))
    if logged_in():
        return '''
        <form method="post">
            <p><textarea name=comment rows="10" cols="80"></textarea>
            <p><input type=submit value=AddComment>
        </form>
        '''

