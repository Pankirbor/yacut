from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import check_request, get_unique_short_id, search_existing_link


@app.route("/api/id/", methods=["POST"])
def create_id():
    """Обработчик запроса на "/api/id/" для
    создания короткой ссылки."""

    data = request.get_json()
    check_request(data)

    new_link = URLMap()
    new_link.from_dict(data)

    if new_link.short is None or new_link.short in ("", " "):
        existing_link = search_existing_link(new_link.original)
        if existing_link:
            short = existing_link.short
        else:
            short = get_unique_short_id()

        new_link.short = short

    db.session.add(new_link)
    db.session.commit()

    return jsonify(new_link.to_dict()), 201


@app.route("/api/id/<short_id>/", methods=["GET"])
def get_url(short_id):
    """Обработчик запроса на "/api/id/<short_id>/" для
    для получения оригинальной ссылки по короткой ссылке."""

    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage("Указанный id не найден", 404)

    return jsonify({"url": link.to_dict()["url"]}), 200
