from typing import cast
from textwrap import dedent
from typing_extensions import LiteralString
from flask import Blueprint, json
from flask import jsonify
from flask import request
from bson import json_util

import os

from imdb.db import get_driver

imdb_api = Blueprint("imdb", "imdb_api")

db = get_driver()
database = os.environ["NEO4J_DATABASE"]


def query(q: LiteralString) -> LiteralString:
    return cast(LiteralString, dedent(q).strip())


@imdb_api.route("/", methods=["GET"])
def fetch_all_movies():
    records, _, _ = db.execute_query(
        query("""
            MATCH (m:Movie)
            RETURN m
        """),
        database_=database,
        routing_="r",
    )

    nodes = []
    for record in records:
        nodes.append(record["m"])

    res = json.loads(json_util.dumps(nodes))
    return jsonify(data=res)


@imdb_api.route("/", methods=["POST"])
def insert_movie():
    data = request.get_json()

    req_body = {}

    if 'title' in data:
        req_body['title'] = data['title']

    if 'year' in data:
        req_body['year'] = data['year']

    if 'votes' in data:
        req_body['votes'] = data['votes']

    if 'runtime' in data:
        req_body['runtime'] = data['runtime']

    if 'revenue' in data:
        req_body['revenue'] = data['revenue']

    if 'rating' in data:
        req_body['rating'] = data['rating']

    if 'movie_id' in data:
        req_body['movie_id'] = data['movie_id']

    if 'description' in data:
        req_body['description'] = data['description']

    if 'actors' in data:
        req_body['actors'] = data['actors']

    if 'directors' in data:
        req_body['directors'] = data['directors']

    if 'genres' in data:
        req_body['genres'] = data['genres']

    res = {}

    records, summary, keys = db.execute_query(
        query("""
            MERGE (m:Movie {title: $prop.title, year: $prop.year, votes: $prop.votes, runtime: $prop.runtime, revenue: $prop.revenue, rating: $prop.rating, movie_id: $prop.movie_id, description: $prop.description })
            WITH *
            UNWIND $prop.actors as actors
            UNWIND $prop.directors as directors
            UNWIND $prop.genres as genres
            MERGE (m) <- [:ACTED_IN] - (a: Person {name: actors})
            MERGE (m) <- [:DIRECTED] - (d: Person {name: directors})
            MERGE (m) - [:IN] -> (g: Genre {genre: genres})
            WITH DISTINCT m
            UNWIND m as movie
            RETURN movie
        """),
        prop=req_body,

        database_=database,
    )

    res = json.loads(json_util.dumps(records))
    return jsonify(data=res)


@imdb_api.route("/<string:id>", methods=["PATCH"])
def update_movie(id):
    if "id" in request.view_args:
        id = request.view_args['id']

    data = request.get_json()

    req_body = {}

    if 'description' in data:
        req_body['description'] = data['description']

    if 'rating' in data:
        req_body['rating'] = data['rating']

    if 'title' in data:
        req_body['title'] = data['title']

    res = {}

    records, summary, keys = db.execute_query(
        query("""
            MATCH (m:Movie {movie_id: $id })
            SET
              m.title = $prop.title, m.description = $prop.description, m.rating = $prop.rating
            
            WITH DISTINCT m
            UNWIND m as movie
            RETURN movie
        """),
        prop=req_body,
        id=id,
        database_=database,
    )

    res = json.loads(json_util.dumps(records))
    return jsonify(data=res)


@imdb_api.route("/<string:id>", methods=["DELETE"])
def delete_movie(id):
    if "id" in request.view_args:
        id = request.view_args['id']

    res = {}

    records, summary, keys = db.execute_query(
        query("""
            MATCH (m:Movie {movie_id: $id })
            DETACH DElETE m
              
            WITH DISTINCT m
            UNWIND m as movie
            RETURN movie
        """),
        id=id,
        database_=database,
    )

    res = json.loads(json_util.dumps(records))
    return jsonify(data=res)


@imdb_api.route("/<string:id>", methods=["GET"])
def fetch_movie(id):
    if "id" in request.view_args:
        id = request.view_args['id']

    records, summary, keys = db.execute_query(
        query("""
            MATCH (m:Movie {movie_id: $id}) -[r] - (a)
            RETURN m, collect(TYPE(r)) as r, collect(a) as childs
        """),
        id=id,
        database_=database,
        routing_="r",
    )

    nodes = []
    for record in records:
        obj = {**record["m"]}
        
        actors = []
        directors = []
        genres = []
        for link, child in zip(record["r"], record["childs"]):
            child = dict(child)
            if link == "ACTED_IN":
                actors.append(child["name"])
            elif link == "DIRECTED":
                directors.append(child["name"])
            else:
                genres.append(child["genre"])
        obj["actors"] = actors
        obj["directors"] = directors
        obj["genres"] = genres

        nodes.append(obj)

    res = json.loads(json_util.dumps({"nodes": nodes}))
    return jsonify(data=res)
