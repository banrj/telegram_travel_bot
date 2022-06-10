from loader import bot
from telebot.types import Message, CallbackQuery
from states.states_for_custom_commands import Info
from keyboards.inline.choice_right_city import city_markup
from keyboards.reply.choice_quantity import button_hotels, button_quantity_photo
from keyboards.reply.choice_photo import button_photo
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from utils.misc.property_request import found_hotels
from keyboards.inline.url_for_hotel import url_markup
from utils.misc.photo_request import take_photo
from datetime import date, timedelta
from loguru import logger


@bot.message_handler(commands=['lowprice', 'highprice', 'beastdeal'])
def answer_low_price(message: Message) -> None:
    """
    Отвечает на команды и запрашивает город поиска отеля.
    :param message: сообщение пользователя
    """
    logger.add('debug_in_command.log', level='DEBUG', format="{time} {level} {message}", rotation="5 KB",
               compression="zip")
    logger.debug('Error')
    logger.info('Information message')
    logger.warning('Warning')
    bot.set_state(message.from_user.id, Info.city)
    bot.send_message(message.chat.id, 'Напишите в каком городе планируйте найти отель \n'
                                      '(<u>на русском</u>)', parse_mode='html')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '/lowprice':
            data['filter'] = "PRICE"
        elif message.text == '/highprice':
            data['filter'] = "PRICE_HIGHEST_FIRST"
        elif message.text == '/beastdeal':
            data['filter'] = "DISTANCE_FROM_LANDMARK"


@bot.message_handler(state=Info.city)
def choice_city(message: Message) -> None:
    """
    Выводит список из инлайн кнопок, проверяет валидность названия города.
    :param message: сообщение пользователя (название города)
    """
    valid = city_markup(message.text)
    if valid:
        bot.send_message(message.from_user.id, 'Уточните пожалуйста!', reply_markup=valid)

    else:
        bot.send_message(message.chat.id, 'Я такого города не знаю, попробуйте еще раз!\n'
                                          'Введите город')
        bot.set_state(message.from_user.id, Info.city)


@bot.callback_query_handler(func=lambda call: call.data.startswith('city_id'))
def check_callback(callback: CallbackQuery) -> None:
    """
    Получает ответ от выбранного города и сохраняет данные, запрашивает начальную цену(если beastdeal) или
    кол-во отелей (lowprice or highprice)
    :param callback: ответ от нажатия на инлайн кнопку(уточнение города)
    """
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        data['city_id'] = callback.data[7:]
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Принято!')
    if data['filter'] == "DISTANCE_FROM_LANDMARK":
        bot.send_message(callback.message.chat.id, 'Введите начальную цену отеля (<u>в долларах $</u>)',
                         parse_mode='html')
        bot.set_state(callback.from_user.id, Info.min_price)
    elif data['filter'] == "PRICE_HIGHEST_FIRST" or data['filter'] == "PRICE":
        bot.send_message(callback.message.chat.id, 'Сколько отелей хотите увидеть?\n'
                                                   'Отелей должно быть <b>не больше 5</b>',
                         reply_markup=button_hotels(),
                         parse_mode='html')
        bot.set_state(callback.from_user.id, Info.quantity_result)


@bot.message_handler(state=Info.quantity_result)
def check_quantity_hotels(message: Message) -> None:
    """
    Получает кол-во отелей, сохраняет эти данные, и спрашивает пользователя про фотографии.
    :param message: сообщение пользователя (кол-во отелей)
    """
    number = message.text

    if number.isdigit():
        if 16 > int(number) > 0:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['quantity_hotels'] = number
            bot.send_message(message.chat.id, 'Принято! Осталось самая малость 😁')
            bot.send_message(message.chat.id, 'Хотите увидеть фотографии для каждого отеля?',
                             reply_markup=button_photo())
            bot.set_state(message.from_user.id, Info.photo)
        else:
            bot.set_state(message.from_user.id, Info.quantity_result)
            bot.send_message(message.chat.id, 'Число должно быть больше 0, но меньше 6\n'
                                              'Попробуйте еще раз 🤧')
    else:
        bot.set_state(message.from_user.id, Info.quantity_result)
        bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
                                          'Попробуйте еще раз 🤧')


@bot.message_handler(state=Info.min_price)
def check_quantity_hotels(message: Message) -> None:
    """
    Функция работает только при bestdeal, получает мин цену, обрабатывает ее и сохраняет.
    Спрашивает у пользователя макс цену.
    :param message: сообщение пользователя (минимальная цена отеля)
    """
    min_price = message.text
    if min_price.isdigit():
        if int(min_price) > 0:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['min_price'] = min_price
            bot.send_message(message.chat.id, 'ОК, теперь максимальную цену (<u>в долларах $</u>) 😁',
                             parse_mode='html')
            bot.set_state(message.from_user.id, Info.max_price)
        else:
            bot.set_state(message.from_user.id, Info.min_price)
            bot.send_message(message.chat.id, 'Число должно быть больше 0\n'
                                              'Попробуйте еще раз 🤧')
    else:
        bot.set_state(message.from_user.id, Info.min_price)
        bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
                                          'Попробуйте еще раз 🤧')


@bot.message_handler(state=Info.max_price)
def check_quantity_hotels(message: Message) -> None:
    """
    Функция работает только при bestdeal, получает макс цену, обрабатывает ее и сохраняет.
    Спрашивает у пользователя минимальное расстояние до центра.
    :param message: сообщение пользователя (максимальная цена отеля)
    """
    max_price = message.text
    if max_price.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(data['min_price']) < int(max_price) > 0:
                data['max_price'] = max_price
                bot.send_message(message.chat.id, 'Cупер, теперь минимальное расстояние до центра <u>в км</u>☺️',
                                 parse_mode='html')
                bot.set_state(message.from_user.id, Info.min_distance_to_center)
            else:
                bot.set_state(message.from_user.id, Info.max_price)
                bot.send_message(message.chat.id, 'Число должно быть больше {limit}\n'
                                                  'Попробуйте еще раз 🤧'.format(limit=data['min_price']))
    else:
        bot.set_state(message.from_user.id, Info.max_price)
        bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
                                          'Попробуйте еще раз 🤧')


@bot.message_handler(state=Info.min_distance_to_center)
def check_quantity_hotels(message: Message) -> None:
    """
    Функция работает только при bestdeal, получает минимальное расстояние, обрабатывает ее и сохраняет.
    Спрашивает у пользователя максимальное расстояние до центра.
    :param message: сообщение пользователя (минимальное расстояние)
    """
    min_distance = message.text
    if min_distance.isdigit():
        if int(min_distance) > -1:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['min_distance'] = min_distance
            bot.send_message(message.chat.id, 'Отлично, теперь максимальное расстояние до центра <u>в км</u> ☺️',
                             parse_mode='html')
            bot.set_state(message.from_user.id, Info.max_distance_to_center)
        else:
            bot.set_state(message.from_user.id, Info.min_distance_to_center)
            bot.send_message(message.chat.id, 'Число должно быть больше либо равно 0\n'
                                              'Попробуйте еще раз 🤧')
    else:
        bot.set_state(message.from_user.id, Info.min_distance_to_center)
        bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
                                          'Попробуйте еще раз 🤧')


@bot.message_handler(state=Info.max_distance_to_center)
def check_quantity_hotels(message: Message) -> None:
    """
    Функция работает только при bestdeal, получает максимальное расстояние, обрабатывает ее и сохраняет.
    Спрашивает у пользователя кол-во отелей.
    :param message: сообщение пользователя (максимальное расстояние)
    """
    max_distance = message.text
    if max_distance.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(data['min_distance']) < int(max_distance) > -1:

                data['max_distance'] = max_distance
                bot.send_message(message.chat.id, 'Сколько отелей хотите увидеть?\n'
                                                  'Отелей должно быть <b>не больше 5</b>', reply_markup=button_hotels(),
                                 parse_mode='html')
                bot.set_state(message.from_user.id, Info.quantity_result)
            else:
                bot.set_state(message.from_user.id, Info.max_distance_to_center)
                bot.send_message(message.chat.id, 'Число должно быть больше {limit}\n'
                                                  'Попробуйте еще раз 🤧'.format(limit=data['min_distance']))
    else:
        bot.set_state(message.from_user.id, Info.max_distance_to_center)
        bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
                                          'Попробуйте еще раз 🤧')


@bot.message_handler(state=Info.photo)
def check_photo(message: Message) -> None:
    """
    Получает сообщение, проверяет его и сохраняет значение.
    Если ответ (да) спрашивает кол-во фотографий.
    Если ответ (нет) спрашивает дату заезда.
    :param message: пользователь отвечает, нужно ли ему вывести фотографии(да/нет)
    """
    if message.text.title().startswith('Да'):
        bot.send_message(message.chat.id, 'Сколько фотографий хотите увидеть на один отель\n'
                                          '<b>не больше 4 фотографий, но не меньше 2</b>',
                         reply_markup=button_quantity_photo(), parse_mode='html')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo'] = True
        bot.set_state(message.from_user.id, Info.quantity_photo)
    elif message.text.title().startswith('Нет'):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo'] = False
            data['quantity_photo'] = 0
        calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today()).build()
        bot.send_message(message.chat.id, 'Нет, так нет 😕')
        bot.send_message(message.chat.id, '📆 Теперь выберите дату заезда', reply_markup=calendar)
    else:
        bot.set_state(message.from_user.id, Info.photo)
        bot.send_message(message.chat.id, 'Я вас не понимаю ответ может быть только вида:\n'
                                          r'Да\Нет, попробуйте еще раз или нажмите кнопку', reply_markup=button_photo())


@bot.message_handler(state=Info.quantity_photo)
def check_quantity_photo(message: Message) -> None:
    """
    Получает число фотографий, проверяет ее и сохраняет.
    Запрашивает дату заезда.
    :param message: число фотографий
    """

    number = message.text
    if number.isdigit():
        if 5 > int(number) > 1:
            calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today()).build()
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['quantity_photo'] = number
            bot.send_message(message.chat.id, '📆 Теперь выберите дату заезда', reply_markup=calendar)
        else:
            bot.set_state(message.from_user.id, Info.quantity_photo)
            bot.send_message(message.chat.id, 'Число должно быть больше 1, но меньше 4\n'
                                              'Попробуйте еще раз 🤧')
    else:
        bot.set_state(message.from_user.id, Info.quantity_photo)
        bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
                                          'Попробуйте еще раз 🤧')


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def take_data_in(callback) -> None:
    """
    Получает дату заезда, проверяет ее и сохраняет.
    Запрашивает дату отъезда.
    :param callback: ответ на нажатия инлайн календаря
    """

    result, key, step = DetailedTelegramCalendar(calendar_id=1,  min_date=date.today()).process(callback.data)
    if not result and key:
        bot.edit_message_text("📆 Выберите {}".format(LSTEP[step]),
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['data_in'] = result
        bot.edit_message_text("Твой выбор {}".format(result),
                              callback.message.chat.id,
                              callback.message.message_id)
        min_out_date = data['data_in'] + timedelta(days=1)
        calendar, step = DetailedTelegramCalendar(calendar_id=2, min_date=min_out_date).build()
        bot.send_message(callback.message.chat.id, '📆 Теперь выбери дату отъезда', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def take_data_out(callback) -> None:
    """
    Получает дату отъезда, проверяет ее и сохраняет.
    Выводит отели.
    :param callback: ответ на нажатия инлайн календаря
    """
    with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
        min_out_date = data['data_in'] + timedelta(days=1)
    result, key, step = DetailedTelegramCalendar(calendar_id=2, min_date=min_out_date).process(callback.data)
    if not result and key:
        bot.edit_message_text("📆 Выберите {}".format(LSTEP[step]),
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
            data['data_out'] = result
        bot.edit_message_text("Твой выбор {}".format(result),
                              callback.message.chat.id,
                              callback.message.message_id)
        bot.delete_state(callback.from_user.id, callback.message.chat.id)

        bot.send_message(callback.message.chat.id, 'Cупер, сейчас покажу отели, которые тебе подойдут!')
        querystring = {"destinationId": data['city_id'],
                       "pageNumber": "1", "pageSize": data['quantity_hotels'],
                       "checkIn": str(data['data_in']), "checkOut": str(data['data_out']),
                       "adults1": "1", "sortOrder": data['filter'], "locale": "ru_RU", "currency": "USD"}
        if data['filter'] == "DISTANCE_FROM_LANDMARK":
            querystring["priceMin"] = data['min_price']
            querystring["priceMax"] = data['max_price']

        total_answer(parameters=querystring, callback=callback, photo=data['photo'], count_photo=data['quantity_photo'])


@logger.catch
def total_answer(parameters: dict, callback: CallbackQuery, photo, count_photo) -> None:
    """
    Получает все сохраненные данные за весь сценарий и выводит отели, проверяет получиться ли найти нужное
    кол-во отелей, и выдает сообщение в каждом из возможных вариантов.
    :param parameters: параметры для property_request
    :param callback: коллбек прошлой функции.
    :param photo: нужно ли фото или нет.
    :param count_photo: кол-во фотографий
    """
    hotels = found_hotels(querystring=parameters)
    if not hotels or len(hotels) == 0:
        bot.send_message(callback.message.chat.id, 'Мы не смогли найти отели по заданным параметрам, '
                                                   'попробуйте еще раз поменяв данные')
        return
    elif len(hotels) < int(parameters['pageSize']):
        bot.send_message(callback.message.chat.id, 'Это все, что мы смогли найти для тебя')
    elif len(hotels) == int(parameters['pageSize']):
        bot.send_message(callback.message.chat.id, 'Вот отели которые тебе подойдут')
    for hotel in hotels:

        if photo:
            bot.send_media_group(callback.message.chat.id, take_photo(hotel['hotel_id'], count_photo))
        bot.send_message(callback.message.chat.id, '📝 Название отеля: {name}\n'
                                                   '🚕 Адреc: {address}\n'
                                                   '👣 Расстояние до центра: {center}\n'
                                                   '💸 Цена за ночь:{price}\n'
                                                   '💵 {total_price}'.format(
                                                    name=hotel['hotel_name'], address=hotel['address'],
                                                    center=hotel['center_distance'], price=hotel['price'],
                                                    total_price=hotel['total_price']),
                         reply_markup=url_markup(hotel['url']))
