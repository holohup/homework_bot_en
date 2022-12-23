from http import HTTPStatus
from json import JSONDecodeError
import logging
import os
import requests
import sys
import time

from dotenv import load_dotenv
import telegram

import exceptions

load_dotenv()

logger = logging.getLogger(__name__)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
RETRY_TIME = 600

HOMEWORK_VERDICTS = {
    'approved': 'Success! The reviewer has approved your homework!',
    'reviewing': 'Your homework is currently being reviewed.',
    'rejected': 'Your homework has been reviewed and needs some improvements.',
}


def send_message(message: str, bot: telegram.Bot) -> None:
    """Sending messages to Telegram."""
    logger.info(f'Trying to send a message: <<{message}>>')

    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)

    except telegram.error.TelegramError as error:
        raise exceptions.TGMessageNotSent(f'Telegram service error: {error}')

    else:
        logger.info(f'Message successfully sent: <<{message}>>')


def get_api_answer(current_timestamp: int) -> dict:
    """Obtaining response from API."""
    params = {
        'url': ENDPOINT,
        'headers': {'Authorization': f'OAuth {PRACTICUM_TOKEN}'},
        'params': {'from_date': current_timestamp},
    }
    logger.info(f'Trying to get an API response. Params: {params}')
    try:
        response = requests.get(**params)
    except requests.exceptions.RequestException as error:
        raise exceptions.RequestFailed(
            f'Could not getch a response from API: {error}'
            f'Parameters: {params}'
        )
    if response.status_code != HTTPStatus.OK:
        raise exceptions.IncorrectStatusCode(
            'Yandex.Practicum API error, '
            f'response code:{response.status_code}'
        )
    logger.info('Response from API successfully obtained.')
    try:
        response = response.json()
    except JSONDecodeError as error:
        raise exceptions.CouldNotParseError(
            f'Could not parse response from json: {error}. '
            f'Server response: {response}'
        )
    return response


def check_response(response: dict) -> list:
    """Parsing the response.
    If everything is correct, returns a homework list."""
    logger.info('Checking server response validity.')
    if not isinstance(response, dict):
        raise TypeError(f'Server response is not a dictionary! {response}')
    try:
        homeworks = response['homeworks']
        response['current_date']
    except KeyError as error:
        raise exceptions.RequiredKeyNotFound(
            f'Required key not found in server response. {error}'
            f'Server response: {response}'
        )
    if not isinstance(homeworks, list):
        raise TypeError('The response value for "homework" key is not a list!')
    logger.info('Server response has been successfully completed.')
    return homeworks


def parse_status(homework: dict) -> str:
    """Parsing API response status."""
    if not isinstance(homework, dict):
        raise TypeError(f'Incorrect homework status format. {homework}')
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
    except KeyError:
        raise KeyError(
            f'Required key(s) not present in the dictionary. '
            f'Dictionary: {homework}'
        )
    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError(
            f'Unknown homework status: {homework_status}'
            f'Dictionary: {homework}'
        )
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Homework status has changed for "{homework_name}": {verdict}'


def check_tokens() -> bool:
    """Returns False if at least one environment variable is missing."""
    logger.info(f'Function {sys._getframe().f_code.co_name} working')
    tokens = (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    return all(tokens)


def main() -> None:
    """Main bot work logic."""
    if not check_tokens():
        message = 'Could not load all required environment variables.'
        logger.critical(message)
        sys.exit(
            f'{message}. Variables:\n'
            f'PRACTICUM_TOKEN: {PRACTICUM_TOKEN}\n'
            f'TELEGRAM_TOKEN: {TELEGRAM_TOKEN}\n'
            f'TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}'
        )

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    previous_error = None

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            current_timestamp = response.get('current_date', current_timestamp)
            if len(homeworks) > 0:
                latest_homework = homeworks[0]
                message = parse_status(latest_homework)
                send_message(message, bot)
            else:
                message = 'No new homework statuses in server response.'
            logger.debug(message)

        except exceptions.NoTelegramError as error:
            error_message = (
                f'We have got an error, '
                f'not sending it to Telegram: {error}'
            )
            logger.error(error_message)

        except Exception as error:
            error_message = f'Homework bot has encountered an error: {error}'
            logger.error(error_message)
            if not isinstance(previous_error, type(error)):
                send_message(error_message, bot)
            previous_error = error

        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s [%(levelname)s] '
            '%(filename)s >> line %(lineno)d '
            '[%(message)s]'
        ),
        handlers=[logging.StreamHandler(stream=sys.stdout)],
    )
    main()
