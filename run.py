from flask import Flask
from web.flaskr import flaskr


app = Flask(__name__)
app.register_blueprint(flaskr)
# app.register_blueprint(admin)


app.debug = True

if __name__ == '__main__':
    app.run()