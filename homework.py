import os
import time
import requests
import logging

import telegram
from dotenv import load_dotenv
from telegram.ext import Updater
from http import HTTPStatus

load_dotenv()


PRACTICUM_TOKEN = os.getenv('TOKEN_P')
TELEGRAM_TOKEN = os.getenv('TOKEN_T')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')
print('ТОКЕНЫЫЫЫЫЫЫЫЫЫЫЫ')
print(PRACTICUM_TOKEN)
print(TELEGRAM_TOKEN)
print(TELEGRAM_CHAT_ID)
print('----------------')
print()

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


def send_message(bot, message):
    """Отправляем сообщение в Telegram чат."""
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logging.info('Функция send_message. Сообщение отправлено.')


def get_api_answer(current_timestamp):
    """Делаем запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    #  timestamp = current_timestamp
    params = {'from_date': timestamp}
    try:
        logging.info('Функция get_api_answer, отправляем api-запрос.')
        answer_homework = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
    except ValueError as error:
        logging.error(f'Функция get_api_answer, ошибка {error}.')
        raise error
    print('ФУНКЦИЯ get_api_answer')
    print(answer_homework)
    print(timestamp)
    print('----------------')
    print()
    get_api_answer_error = (
        f'Функция get_api_answer, ошибка {answer_homework.status_code}.'
    )
    if answer_homework.status_code == HTTPStatus.OK:
        return answer_homework.json()
    else:
        raise TypeError(get_api_answer_error)


def check_response(response):
    """Проверяем ответ API на корректность."""
    logging.info(
        'Функция check_response, проверяем ответ API на корректность.'
    )
    print('ФУНКЦИЯ check_response')
    try:
        response = response['homeworks']
        print('1', response)
    except KeyError:
        logging.error('Функция check_response, неверный ключ.')
        response = None
    try:
        response = response[0]
        print('2', response)
    except IndexError:
        logging.error('Функция check_response, неверный индекс.')
        response = None
    print('3', response)
    print(type(response))
    print('----------------')
    print()
    if type(response) == dict:
        return response
    logging.error('Функция check_response, неверный тип возвращаемых данных.')
    return None


def parse_status(homework):
    """Из информации о конкретной домашней работе извдекаем статус."""
    logging.info(
        'Функция parse_status, извлекли информацию о конкретной работе.'
    )

    #  homework = homework[0]
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
        verdict = HOMEWORK_STATUSES[homework_status]
    except KeyError:
        homework_name = None
    except TypeError:
        homework_name = None
    if 'homework_name' not in homework:
        logging.error(
            'Функция parse_status, homework_name отсутствует в homework'
        )
        raise KeyError(
            'Функция parse_status, homework_name отсутствует в homework'
        )
    if homework_status not in HOMEWORK_STATUSES:
        raise Exception
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяем доступность переменных окружения,
    которые необходимы для работы программы.
    """
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID is not None:
        logging.info('Функция check_tokens, переменные окружения доступны.')
        return True
    logging.critical('Функция check_tokens, переменные окружения не доступны.')
    return False


def main():
    """Основная логика работы бота.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    #  current_timestamp = 0
    current_timestamp = 1650130498
    check_tokens()
    print('ФУНКЦИЯ main')
    print(check_tokens())
    print('----------------')
    print()
    error_message = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            result_check_response = check_response(response)
            message = parse_status(result_check_response)

            current_timestamp = response.get('current_date', current_timestamp)
            if result_check_response:
                send_message(bot, parse_status(result_check_response))
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            if message not in error_message:
                error_message = message
                logging.critical(message)
                send_message(bot, message)
            #  logging.error(message)
            time.sleep(RETRY_TIME)
        else:
            send_message(bot, message)
            updater = Updater(token=TELEGRAM_TOKEN)
            updater.start_polling(poll_interval=RETRY_TIME)
            updater.idle()


if __name__ == '__main__':
    main()
