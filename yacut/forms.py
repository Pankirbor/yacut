from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class URLForm(FlaskForm):
    """Класс описания формы с валидацией данных."""

    original_link = URLField(
        "Введите оригинальную ссылку",
        validators=[DataRequired(message="Обязательное поле"), Length(1, 256)],
    )
    custom_id = URLField(
        "Ваш вариант короткой ссылки", validators=[Optional(), Length(1, 16)]
    )
    submit = SubmitField("Создать")
