import json
from pathlib import Path
from flask import render_template, request, redirect, url_for, abort, Blueprint
from flask_paginate import Pagination
from nannaElise.models import Post

main = Blueprint("main", __name__)


@main.route("/")
def base():
    """Redirect base url to home"""
    return redirect(url_for("main.home"))


@main.route("/home")
def home():
    title = "Home"
    return render_template("home.html", title=title)


@main.route("/videos")
def videos():
    title = "Videos"
    video_json_path = Path(__file__).parent / f"../static/videos.json"
    with open(video_json_path) as readfile:
        video_json = json.load(readfile)
        video_json["videos"] = video_json["videos"][
            :12
        ]  # load only 12 videos for now... iframe lag
    if not video_json:
        abort(404)
    return render_template("videos.html", title=title, video_json=video_json)


@main.route("/recipes")
def recipes():
    title = "Recipes"
    return render_template("recipes.html", title=title)


@main.route("/blog")
def blog():
    title = "Blog"
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("blog.html", title=title, posts=posts)
