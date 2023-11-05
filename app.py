from flask import Flask, jsonify, make_response, redirect
from imdb import routes


app = Flask(__name__)

app.register_blueprint(routes.imdb_api, url_prefix='/imdb')


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
