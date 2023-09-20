from random import choices
from string import digits, ascii_letters

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db

SIMBOLS = digits + ascii_letters
HOST = "http://127.0.0.1:5000/"


def get_unique_short_id():
    tail = "".join(choices(SIMBOLS, k=6))
    return HOST + tail


@app.route("/")
def index_view():
    return render_template("yacut.html")
