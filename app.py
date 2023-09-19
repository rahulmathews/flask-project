from flask import Flask, redirect

from netflix import db, routes

app = Flask(__name__)

app.register_blueprint(routes.netflix_api, url_prefix='/netflix')


@app.route("/")
def index():
    return redirect('/ping')


@app.route("/ping")
def ping():
    return "pong"
