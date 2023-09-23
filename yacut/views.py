from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, search_existing_link


@app.route("/", methods=["POST", "GET"])
def index_view():
    """Обработчик для главной страницы сайта."""

    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_link = form.custom_id.data

        if custom_link:
            if URLMap.query.filter_by(short=custom_link).first():
                flash(f"Имя {custom_link} уже занято!", category="error")
                return render_template("yacut.html", form=form)

            new_link = URLMap(original=original_link, short=custom_link)
        else:
            existing_link = search_existing_link(original_link)

            if existing_link:
                return render_template("yacut.html", form=form, new_link=existing_link)

            short_link = get_unique_short_id()
            new_link = URLMap(original=original_link, short=short_link)

        db.session.add(new_link)
        db.session.commit()
        flash("Ссылка успешно создана ;)", category="done")

        return render_template("yacut.html", form=form, new_link=new_link)

    return render_template("yacut.html", form=form)


@app.route("/<path:short_link>")
def redirect_original_link(short_link):
    """Обработчик для перенаправления на сайт по оригинальной ссылке."""

    link = URLMap.query.filter_by(short=short_link).first()
    if not link:
        abort(404)
    return redirect(link.original)
