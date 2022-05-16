def get_api_answer(current_timestamp):
    """Делаем запрос к единственному эндпоинту API-сервиса.
    """
    #timestamp = current_timestamp or int(time.time())
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    answer_homework = requests.get(ENDPOINT, headers=HEADERS, params=params)
    print(answer_homework)
    print(timestamp)
    print('----------------')
    if str(answer_homework) == '<Response [200]>':
        answer_homework = answer_homework.json()
        return answer_homework
    answer_homework = False
    print(answer_homework)
    print('----------------')
    return answer_homework

def get_api_answer(current_timestamp):
    """Делаем запрос к единственному эндпоинту API-сервиса.
    """
    #timestamp = current_timestamp or int(time.time())
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    answer_homework = requests.get(ENDPOINT, headers=HEADERS, params=params)
    print('ФУНКЦИЯ get_api_answer')
    print(answer_homework)
    print(timestamp)
    print('----------------')
    print()
    if answer_homework.status_code == HTTPStatus.OK:
        answer_homework = answer_homework.json()
        return answer_homework
    
    elif answer_homework.status_code == HTTPStatus.NOT_FOUND:
        print('ERORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
        return TypeError
    elif answer_homework.status_code != HTTPStatus.OK:
        return TypeError




def check_tokens():
    """Проверяем доступность переменных окружения,
    которые необходимы для работы программы.
    """
    if 'TOKEN_P' and 'TOKEN_T' and 'CHAT_ID' in os.environ:
    if os.environ['TOKEN_P'] == PRACTICUM_TOKEN and os.environ['TOKEN_T'] == TELEGRAM_TOKEN and os.environ['CHAT_ID'] == TELEGRAM_CHAT_ID:
        return True
    return False




def check_response(response):
    """Проверяем ответ API на корректность.
    """
    try:
        response = response['homeworks']
        response = response[0]
    except KeyError:
        response = False
    except IndexError:
        response = False
    print('ФУНКЦИЯ check_response')
    print(response)
    print(type(response))
    print('----------------')
    print()
    if type(response) == dict:
        return response
    return False




def main():
    """Основная логика работы бота.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0 
    #current_timestamp = int(time.time())

    check_tokens()
    print('ФУНКЦИЯ main')
    print(check_tokens())
    print('----------------')
    print()
    result_get_api_answer = get_api_answer(current_timestamp)
    result_check_response = check_response(result_get_api_answer)
    result_parse_status = parse_status(result_check_response)
    send_message(bot, result_parse_status)


    updater = Updater(token=TELEGRAM_TOKEN)
    updater.start_polling(poll_interval=RETRY_TIME)
    updater.idle()
    ...



    ...

    while True:
        try:
            response = ...

            ...

            current_timestamp = ...
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
        else:
            ...


if __name__ == '__main__':
    main()




    print('ФУНКЦИЯ parse_status')
    print(homework)
    print(homework_name)
    print(homework_status)
    print(verdict)
    print('----------------')
    print()