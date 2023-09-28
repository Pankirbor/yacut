from string import ascii_letters, digits

HOST = "http://localhost/"
SIMBOLS = digits + ascii_letters
PATTERN_VALID_SHORT_NAME = r"[\W\sА-я]+"
PATTERN_REGEXP_VALIDATOR = r"[^\W\sА-я\s]+$"
MAX_LENGTH_SHORT_NAME = 16
MAX_LENGTH = 256
MIN_LENGTH = 1
KEYS_DATA = ("url", "custom_id")
KEYS_TO_DICT = ("url", "short_link")
MODEL_FIELDS = dict(url="original", custom_id="short")

# error message text
MISSING_DATA_MSG = "Отсутствует тело запроса"
INVALID_NAME_MSG = "Указано недопустимое имя для короткой ссылки"
URL_REQUIRED_MSG = '"url" является обязательным полем!'
DUPLICATE_NAME_MSG = "Имя {short} уже занято{punctuation}"
ACCEPT = "Ссылка успешно создана ;)"
NOT_FOUND = "Указанный id не найден"
HELP_TEXT_ORIGINAL_LINK = "Введите оригинальную ссылку."
HELP_TEXT_SHORT_LINK = "Ваш вариант короткой ссылки."
ERROR_REQUIRED_FIELD = "Это поле обязательно к заполнению."
SUBMIT_BUTTON = "Создать"
