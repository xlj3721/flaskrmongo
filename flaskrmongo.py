# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from flask.ext.mongoalchemy import MongoAlchemy


# create our little application :)
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['MONGOALCHEMY_DATABASE'] = 'weibo'
app.config['SECRET_KEY']='development key'
app.config['USERNAME']='admin'
app.config['PASSWORD']='default'

db = MongoAlchemy(app)

class Twitter(db.Document):
    title = db.StringField()
    text = db.StringField()



@app.route('/')
def show_entries():
    
    entries = Twitter.query.all()
    return render_template('show_entries.html', entries=entries)



@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    

    entrie = Twitter(title=request.form['title'],text=request.form['text'])
    entrie.save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    print 'hello xlj3721'
    app.run()
