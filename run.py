# -*- coding: utf-8 -*-
from flask import Flask

from admin.view import admin
from front.view  import front

app  = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint( front )

if __name__ == '__main__':
    app.run(
    host = '127.0.0.1',
    port = 5001,
    debug = True
    )
