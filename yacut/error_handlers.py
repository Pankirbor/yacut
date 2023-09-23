from flask import render_template, jsonify

from yacut import app, db


class InvalidAPIUsage(Exception):
    """Класс исключений при обращении к api проекта."""

    status_code = 404

    def __init__(self, message, status_code=None) -> None:
        """Инициализатор объекта класса."""

        super().__init__()

        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        """Метод для преобразования
        атрибутов объекта в словарь."""

        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик исключений при
    работе с api проекта."""

    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Обработчик исключений 404."""

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработчик исключений 500."""

    db.session.rollback()
    return render_template("500.html"), 500
