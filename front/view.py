# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, request, session, g, redirect, url_for, abort,\
render_template, flash
from pymongo import MongoClient


front = Blueprint(
    'front',
    '__name__',
    template_folder='templates/front',
    static_folder='static/front'
    )

def connect_db():
    """Connects to the specific database."""
    client = MongoClient('localhost', 27017)
    print('连接成功')
    db_name = client.conn
    collection = db_name.conn
    db = collection
    return db

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mongo_db'):
        g.mongo_db = connect_db()
    return g.mongo_db

def close_db(error):
    if hasattr(g, 'mongo_db'):
        g.mongo_db.close()

@front.before_request
def before_request():
    g.db = connect_db()

# @front.teardown_request
# def teardown_request(exception):
#     g.db.close()


@front.route('/')
def show_entries():
    db = get_db()
    cur = db.find({})
    entries = cur
    return render_template("show_entries.html", entries = entries)


@front.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title= request.form['title']
    text = request.form['text']
    g.db.insert({'title': title, 'text': text})
    flash('New entry was successfully posted')
    return redirect(url_for('.show_entries'))


@front.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != 'admin':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('.show_entries'))
    return render_template("login.html", error = error)

@front.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('.show_entries'))
