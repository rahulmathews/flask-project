from flask import Blueprint, json
from flask import flash
from flask import g
from flask import redirect
from flask import jsonify
from flask import request
from flask import url_for
from bson import json_util

from netflix.db import get_db

netflix_api = Blueprint("netflix", "netflix_api")


@netflix_api.route("/", methods=["GET"])
def index():
    db = get_db()
    movies = []
    for movie in db['movies'].find({}):
        movies.append(movie)

    movies = json.loads(json_util.dumps(movies))

    return jsonify(movies=movies)


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )


@netflix_api.route("/create", methods=["GET", "POST"])
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))


@netflix_api.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (
                    title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))


@netflix_api.route("/<int:id>/delete", methods=["POST",])
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
