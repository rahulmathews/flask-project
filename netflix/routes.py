from flask import Blueprint, json
from flask import flash
from flask import g
from flask import redirect
from flask import jsonify
from flask import request
from flask import url_for
from bson import ObjectId, json_util

from netflix.db import get_db

netflix_api = Blueprint("netflix", "netflix_api")

db = get_db()


@netflix_api.route("/", methods=["GET"])
def fetch_all_movies():
    movies = []
    for movie in db['movies'].find({}):
        movies.append(movie)

    movies = json.loads(json_util.dumps(movies))

    return jsonify(movies=movies)


@netflix_api.route("/", methods=["POST"])
def insert_movie():
    data = request.get_json()

    req_body = {}

    if 'age_certification' in data:
        req_body['age_certification'] = data['age_certification']

    if 'description' in data:
        req_body['description'] = data['description']

    if 'genres' in data:
        req_body['genres'] = data['genres']

    if 'id' in data:
        req_body['id'] = data['id']

    if 'imdb_score' in data:
        req_body['imdb_score'] = data['imdb_score']

    if 'production_countries' in data:
        req_body['production_countries'] = data['production_countries']

    if 'release_year' in data:
        req_body['release_year'] = data['release_year']

    if 'runtime' in data:
        req_body['runtime'] = data['runtime']

    if 'title' in data:
        req_body['title'] = data['title']

    if 'type' in data:
        req_body['type'] = data['type']

    res = {}

    result = db['movies'].insert_one(req_body)

    res['id'] = json.loads(json_util.dumps(result.inserted_id))

    return jsonify(data=res)


@netflix_api.route("/<string:id>", methods=["PATCH"])
def update_movie(id):
    if "id" in request.view_args:
        id = request.view_args['id']

    data = request.get_json()

    req_body = {}

    if 'description' in data:
        req_body['description'] = data['description']

    if 'id' in data:
        req_body['id'] = data['id']

    if 'imdb_score' in data:
        req_body['imdb_score'] = data['imdb_score']

    if 'runtime' in data:
        req_body['runtime'] = data['runtime']

    if 'title' in data:
        req_body['title'] = data['title']

    result = db['movies'].find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": req_body}, new=True)

    res = json.loads(json_util.dumps(result))

    return jsonify(data=res)


@netflix_api.route("/<string:id>", methods=["DELETE"])
def delete_movie(id):
    if "id" in request.view_args:
        id = request.view_args['id']

    result = db['movies'].find_one_and_delete(
        {"_id": ObjectId(id)})

    res = json.loads(json_util.dumps(result))

    return jsonify(data=res)


@netflix_api.route("/<string:id>", methods=["GET"])
def fetch_movie(id):
    if "id" in request.view_args:
        id = request.view_args['id']

    result = db['movies'].find_one(
        {"_id": ObjectId(id)})

    res = json.loads(json_util.dumps(result))

    return jsonify(data=res)
