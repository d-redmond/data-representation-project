#!flask/bin/python

from flask import Flask, render_template
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from family.family_members import family_members_table
from login.login import log

app = Flask(__name__, static_folder="main/static",
            template_folder="main/template")
app.secret_key = 'anyKey'
app.register_blueprint(family_members_table, url_prefix="/family/")
app.register_blueprint(log, url_prefix="/login")

@app.route('/')
def home():
    return render_template("index.html")

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'Error: Bad Request', 400

@app.errorhandler(NotFound)
def handle_bad_request(e):
    return 'Error: Page Not Found', 404

@app.errorhandler(InternalServerError)
def handle_bad_request(e):
    return 'Internal server error!', 500

if __name__ == '__main__':
    app.run(debug=True)