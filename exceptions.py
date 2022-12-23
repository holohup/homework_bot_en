class NoTelegramError(BaseException):
    """Класс, чтобы наследовать от него исключения, не требующие.
    отправки сообщения в телеграм.
    """


class CriticalError(NoTelegramError):
    """Критическая ошибка в работе робота."""


class IncorrectStatusCode(Exception):
    """Статус ответа сервера API не равен 200."""


class EmptyDictionaryError(Exception):
    """Пустой словарь."""


class RequestFailed(NoTelegramError):
    """Не получилось получить данные методом requests.get."""


class NotFoundError(Exception):
    """Что-то не найдено."""


class ServiceUnavailableError(Exception):
    """Сервис недоступен."""


class TGMessageNotSent(NoTelegramError):
    """Не удалось отправить сообщение."""


class CouldNotParseError(Exception):
    """Не удалось распарсить ответ."""


class RequiredKeyNotFound(NoTelegramError):
    """В словаре не найдет необходимый ключ."""
