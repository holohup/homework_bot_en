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
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(message: str, bot: telegram.Bot) -> None:
    """Отправка сообщения в телеграм."""
    logger.info(
        f'Попытка отправить сообщение: <<{message}>>'
    )

    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)

    except telegram.error.TelegramError as error:
        raise exceptions.TGMessageNotSent(
            f'Ошибка в работе с сервисом telegram: {error}'
        )

    else:
        logger.info(
            f'Сообщение успешно отправлено: <<{message}>>'
        )


def get_api_answer(current_timestamp: int) -> dict:
    """Получение ответа от API и его проверка."""
    params = {
        'url': ENDPOINT,
        'headers': {'Authorization': f'OAuth {PRACTICUM_TOKEN}'},
        'params': {'from_date': current_timestamp}
    }
    logger.info(f'Попытка получить информацию от API. Параметры: {params}')
    try:
        response = requests.get(**params)
    except requests.exceptions.RequestException as error:
        raise exceptions.RequestFailed(
            f'Не удалось получить ответ от API: {error}'
            f'Параметры запроса: {params}'
        )
    if response.status_code != HTTPStatus.OK:
        raise exceptions.IncorrectStatusCode(
            'Ошибка при работе с Я.сервером, '
            f'код ответа:{response.status_code}'
        )
    logger.info('Ответ от API успешно получен.')
    try:
        response = response.json()
    except JSONDecodeError as error:
        raise exceptions.CouldNotParseError(
            f'Не удается распарсить ответ из json: {error}. '
            f'Ответ сервера: {response}'
        )
    return response


def check_response(response: dict) -> list:
    """Разбираем ответ сервера и если все ОК, возвращаем список домашек."""
    logger.info('Проверяем валидность ответа сервера.')
    if not isinstance(response, dict):
        raise TypeError(f'Ответ сервера - не словарь! {response}')
    try:
        homeworks = response['homeworks']
        response['current_date']
    except KeyError as error:
        raise exceptions.RequiredKeyNotFound(
            f'Нет необходимого ключа в ответе сервера. {error}'
            f'Ответ сервера: {response}'
        )
    if not isinstance(homeworks, list):
        raise TypeError(
            'В ответе от API под ключом "homeworks" пришел не список'
        )
    logger.info('Проверка ответа сервера успешно завершена.')
    return homeworks


def parse_status(homework: dict) -> str:
    """Распарсивание ответа API."""
    if not isinstance(homework, dict):
        raise TypeError(
            f'Домашнее задание не в правильном формате. {homework}'
        )
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
    except KeyError:
        raise KeyError(
            f'В словаре нету нужного(ых) ключа(ей). Словарь: {homework}'
        )
    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError(
            f'Неизвестный статус домашнего задания: {homework_status}'
            f'Словарь: {homework}'
        )
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens() -> bool:
    """Если хотя бы одной переменной нет в окружении, вернет False."""
    logger.info(f'Вызвана функция {sys._getframe().f_code.co_name}')
    tokens = (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    return all(tokens)


def main() -> None:
    """Основная логика работы бота."""
    if not check_tokens():
        message = 'Не удалось загрузить все переменные из окружения.'
        logger.critical(message)
        sys.exit(
            f'{message}. Переменные:\n'
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
            current_timestamp = response.get(
                'current_date', current_timestamp
            )
            if len(homeworks) > 0:
                latest_homework = homeworks[0]
                message = parse_status(latest_homework)
                send_message(message, bot)
            else:
                message = 'Нет новых статусов в ответе сервера.'
            logger.debug(message)

        except exceptions.NoTelegramError as error:
            error_message = f'Ошибка без отправки в телеграм: {error}'
            logger.error(error_message)

        except Exception as error:
            error_message = f'Сбой в работе программы: {error}'
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
        handlers=[logging.StreamHandler(stream=sys.stdout)]
    )
    main()
