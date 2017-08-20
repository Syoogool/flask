# -*- coding: utf-8 -*-

import os
import sqlite3
from pymongo import MongoClient
from flask import Flask, Blueprint, request, session, g, redirect, url_for, abort,\
render_template, flash

app = Flask(__name__)
app.debug = True
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# app.config.from_object(__name__)
#  配置 设置环境变量 FLASKR_SETTINGS 为 f:\2017\flask\flaskr\settings.cfg
# flaskr = Blueprint('flaskr', __name__, template_folder='templates')
def connect_db():
    """Connects to the specific database."""
    # rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    # return rv

    client = MongoClient('localhost', 27017)
    print('连接成功')

    # 连接数据库  test数据库名
    db_name = client.conn

    # 连接所有集合（表）
    collection = db_name.conn
    db = collection

    return db

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# 初始化数据库
# with app.app_context()建立应用环境
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read(),)
        db.commit()

# @err 原因，全局变量g.db没有定义，在系统启动前增加全局变量即可
@app.before_request
def before_request():
    g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
#     g.db.close()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.find({})
    # entries = cur.fetchall()
    entries = cur
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    # g.db.execute('insert into entries (title, text) values (?, ?)',
    #              [request.form['title'], request.form['text']])
    title= request.form['title']
    text = request.form['text']
    g.db.insert({'title': text, 'text': text})
    # g.db.save()
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
    app.run()