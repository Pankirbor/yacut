import re

from random import choices
from string import ascii_letters, digits

from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap

SIMBOLS = digits + ascii_letters


def get_unique_short_id():
    """Функция для генерации уникального идентификатора
    короткой ссылки."""

    short_link = None

    while True:
        short_link = "".join(choices(SIMBOLS, k=6))
        if not URLMap.query.filter_by(short=short_link).first():
            break

    return short_link


def search_existing_link(original_link):
    """Функция поиска уже существующей записи
    в базе данных с переданной оригинальной ссылкой."""

    link = URLMap.query.filter_by(original=original_link).first()
    if link:
        return link


def check_request(data):
    """Функция проверки корректности
    вводимых данных пользователя для короткой ссылки."""

    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса", 400)

    if "url" not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            400,
        )

    if "custom_id" in data and data["custom_id"]:
        if len(data["custom_id"]) == 0 or len(data["custom_id"]) > 16:
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки",
                400,
            )

        if URLMap.query.filter_by(short=data["custom_id"]).first():
            raise InvalidAPIUsage(
                f'Имя "{data["custom_id"]}" уже занято.',
                400,
            )

        if re.search(r"[\W\sА-я]+", data["custom_id"]):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки",
                400,
            )
