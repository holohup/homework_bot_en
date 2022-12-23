class NoTelegramError(BaseException):
    """Base parent class for all the exceptions that don't need to be
    sent to Telegram.
    """


class CriticalError(NoTelegramError):
    """Critical error."""


class IncorrectStatusCode(Exception):
    """Server response status code is not 200."""


class EmptyDictionaryError(Exception):
    """The response dictionary is empty."""


class RequestFailed(NoTelegramError):
    """Could not fetch data using requests.get."""


class NotFoundError(Exception):
    """Something isn't found."""


class ServiceUnavailableError(Exception):
    """Service is unavailable."""


class TGMessageNotSent(NoTelegramError):
    """Could not send a message."""


class CouldNotParseError(Exception):
    """The response could not be parsed."""


class RequiredKeyNotFound(NoTelegramError):
    """Required key not found in the dictionary."""
