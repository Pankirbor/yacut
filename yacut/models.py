from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Класс описывающий таблицу для базы данных."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False, unique=True)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Метод для преобразования объекта класса в словарь."""

        return dict(
            url=self.original,
            short_link="http://localhost/" + self.short,
        )

    def from_dict(self, data):
        """Метод присвоения атрибутам объекта значений из словаря."""

        model_fields = dict(url="original", custom_id="short")
        for field in ["url", "custom_id"]:
            if field in data:
                setattr(self, model_fields[field], data[field])
