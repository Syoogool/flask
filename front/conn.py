# -*- coding: utf-8 -*-
from pymongo import MongoClient

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

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
