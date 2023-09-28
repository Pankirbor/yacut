from flask import jsonify, request

from yacut import app
from yacut.constants import NOT_FOUND
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


@app.route("/api/id/", methods=["POST"])
def create_id():
    """Обработчик запроса на "/api/id/" для
    создания короткой ссылки."""

    data = request.get_json()
    try:
        new_link = URLMap.create(data)

    except Exception as err:
        raise InvalidAPIUsage(str(err), 400)

    return jsonify(new_link.to_dict()), 201


@app.route("/api/id/<short_id>/", methods=["GET"])
def get_url(short_id):
    """Обработчик запроса на "/api/id/<short_id>/" для
    для получения оригинальной ссылки по короткой ссылке."""

    link = URLMap.get_link(short_id)
    if not link:
        raise InvalidAPIUsage(NOT_FOUND, 404)

    return jsonify({"url": link.to_dict()["url"]}), 200
