import re

from datetime import datetime
from random import choices

from yacut import db
from yacut.exceptions import InvalidDataError, InvalidShortNameException
from yacut.constants import (
    DUPLICATE_NAME_MSG,
    HOST,
    INVALID_NAME_MSG,
    KEYS_DATA,
    KEYS_TO_DICT,
    LENGTH_GENERATE_SHORT_NAME,
    MAX_LENGTH,
    MAX_LENGTH_SHORT_NAME,
    MISSING_DATA_MSG,
    MODEL_FIELDS,
    PATTERN_VALID_SHORT_NAME,
    SIMBOLS,
)


class URLMap(db.Model):
    """Класс описывающий таблицу для базы данных."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH), nullable=False, unique=True)
    short = db.Column(db.String(MAX_LENGTH_SHORT_NAME), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __setattr__(self, key, value):
        """Метод контролирующий присваивание значений атрибутам
        с предварительной проверкой корректности данных для короткой ссылки."""

        if key == "short":
            if value in ("", " ", None):
                value = None
            elif len(value) > MAX_LENGTH_SHORT_NAME or re.search(
                PATTERN_VALID_SHORT_NAME, value
            ):
                raise InvalidShortNameException(INVALID_NAME_MSG)

            elif URLMap.get_link(value):
                raise InvalidShortNameException(DUPLICATE_NAME_MSG)

        super().__setattr__(key, value)

    def to_dict(self):
        """Метод для преобразования объекта класса в словарь."""

        attrs_name = list(MODEL_FIELDS.values())
        attrs_val = (getattr(self, attrs_name[0]), HOST + getattr(self, attrs_name[1]))

        return dict(zip(KEYS_TO_DICT, attrs_val))

    def from_dict(self, data):
        """Метод присвоения атрибутам объекта значений из словаря."""

        if not data:
            raise InvalidDataError(MISSING_DATA_MSG)

        if "url" not in data:
            raise InvalidDataError(
                '"url" является обязательным полем!',
            )
        for field in KEYS_DATA:
            if field in data:
                setattr(self, MODEL_FIELDS[field], data[field])

    def save(self):
        """Метод для сохранения объекта в базе данных."""

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_unique_short_id(cls):
        """Метод для генерации уникального идентификатора
        короткой ссылки."""

        short_link = None

        while True:
            short_link = "".join(
                choices(
                    SIMBOLS,
                    k=LENGTH_GENERATE_SHORT_NAME,
                )
            )
            if not cls.get_link(short_link):
                break

        return short_link

    @classmethod
    def create(cls, *args, **kwargs):
        """Публичный метод для создания объекта модели."""

        if kwargs:
            new_link = URLMap(**kwargs)
        else:
            new_link = URLMap()
            new_link.from_dict(args[0])

        if not new_link.short:
            existing_link = cls.get_link(new_link.original, short=False)
            if existing_link:
                return existing_link

            new_link.short = cls.get_unique_short_id()
        new_link.save()

        return new_link

    @classmethod
    def get_link(cls, link, short=True):
        """Метод получения объекта модели
        по атрибуту короткой ссылки по умолчанию,
        либо по атрибуту длинной ссылки с параметром short=False."""

        if short:
            return cls.query.filter(URLMap.short == link).first()

        return cls.query.filter(URLMap.original == link).first()
