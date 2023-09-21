from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, search_existing_link


@app.route("/api/id/", methods=["POST"])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)

    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    if "custom_id" in data and len(data["custom_id"]) == 0:
        raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки", 400)

    if "custom_id" in data:
        if len(data["custom_id"]) == 0 or len(data["custom_id"]) > 16:
            raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки", 400)

        if URLMap.query.filter_by(short=data["custom_id"]).first():
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.', 400)

    new_link = URLMap()
    new_link.from_dict(data)

    if not new_link.short:
        all_links = URLMap.query.all()
        existing_link = search_existing_link(all_links, new_link.original)
        if existing_link:
            short = existing_link.short
        else:
            short = get_unique_short_id(all_links)

        new_link.short = short

    db.session.add(new_link)
    db.session.commit()

    return jsonify(new_link.to_dict()), 201


@app.route("/api/id/<short_id>/", methods=["GET"])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage("Указанный id не найден", 404)

    return jsonify({"url": link.to_dict()["url"]}), 200
