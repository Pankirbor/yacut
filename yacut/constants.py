from string import ascii_letters, digits

HOST = "http://localhost/"
SIMBOLS = digits + ascii_letters
PATTERN_VALID_SHORT_NAME = r"[\W\sА-я]+"
MAX_LENGTH_SHORT_NAME = 16
MIN_LENGTH_SHORT_NAME = 1
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
