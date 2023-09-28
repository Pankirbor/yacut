from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Regexp

from yacut.constants import (
    ERROR_REQUIRED_FIELD,
    HELP_TEXT_ORIGINAL_LINK,
    HELP_TEXT_SHORT_LINK,
    INVALID_NAME_MSG,
    MAX_LENGTH,
    MAX_LENGTH_SHORT_NAME,
    MIN_LENGTH,
    PATTERN_REGEXP_VALIDATOR,
    SUBMIT_BUTTON,
)


class URLForm(FlaskForm):
    """Класс описания формы с валидацией данных."""

    original_link = URLField(
        HELP_TEXT_ORIGINAL_LINK,
        validators=[
            DataRequired(message=ERROR_REQUIRED_FIELD),
            Length(MIN_LENGTH, MAX_LENGTH),
        ],
    )
    custom_id = URLField(
        HELP_TEXT_SHORT_LINK,
        validators=[
            Optional(),
            Length(MIN_LENGTH, MAX_LENGTH_SHORT_NAME),
            Regexp(PATTERN_REGEXP_VALIDATOR, message=INVALID_NAME_MSG),
        ],
    )
    submit = SubmitField(SUBMIT_BUTTON)
