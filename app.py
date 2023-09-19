from flask import Flask, jsonify, make_response, redirect
from netflix import db, routes


app = Flask(__name__)

app.register_blueprint(routes.netflix_api, url_prefix='/netflix')


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.route("/")
def index():
    return redirect('/ping')


@app.route("/ping")
def ping():
    return "pong"


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
