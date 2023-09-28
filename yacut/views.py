from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.constants import DUPLICATE_NAME_MSG, ACCEPT
from yacut.models import URLMap
from yacut.forms import URLForm


def get_params(form):
    params = dict(original=form.original_link.data, short=form.custom_id.data)
    return params


@app.route("/", methods=["POST", "GET"])
def index_view():
    """Обработчик для главной страницы сайта."""

    form = URLForm()
    if form.validate_on_submit():
        params = get_params(form)
        if params["short"]:
            if URLMap.get_link(params["short"]):
                flash(
                    DUPLICATE_NAME_MSG.format(short=params["short"], punctuation="!"),
                    category="error",
                )
                return render_template("yacut.html", form=form)

        new_link = URLMap.create(**params)
        flash(ACCEPT, category="done")

        return render_template("yacut.html", form=form, new_link=new_link)

    return render_template("yacut.html", form=form)


@app.route("/<path:short_link>")
def redirect_original_link(short_link):
    """Обработчик для перенаправления на сайт по оригинальной ссылке"""

    link = URLMap.get_link(short_link)
    if not link:
        abort(404)
    return redirect(link.original)
