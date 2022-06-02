from loader import bot
from telebot.types import Message, CallbackQuery
from states.states_for_custom_commands import Info
from keyboards.inline.choice_right_city import city_markup_high
from keyboards.reply.choice_quantity import button_hotels, button_quantity_photo
from keyboards.reply.choice_photo import button_photo
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from utils.misc.property_request import found_hotels
from keyboards.inline.url_for_hotel import url_markup
from utils.misc.photo_request import take_photo


# @bot.message_handler(commands=['highprice'])
# def answer_low_price(message: Message) -> None:
#     bot.set_state(message.from_user.id, HighInfo.city_high)
#     bot.send_message(message.chat.id, 'Напишите в каком городе планируйте найти дорогой отель')
#

# @bot.message_handler(state=HighInfo.city_high)
# def choice_city(message: Message) -> None:
#     valid = city_markup_high(message.text)
#     if valid:
#         bot.send_message(message.from_user.id, 'Уточните пожалуйста!', reply_markup=valid)
#
#     else:
#         bot.send_message(message.chat.id, 'Я такого города не знаю, попробуйте еще раз!\n'
#                                           'Введите город')
#         bot.set_state(message.from_user.id, HighInfo.city_high)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith('Hcity_id'))
# def check_callback_high(callback: CallbackQuery) -> None:
#     with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
#         data['city_id'] = callback.data[8:]
#     bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Принято!')
#     bot.send_message(callback.message.chat.id, 'Сколько отелей хотите увидеть?\n'
#                                                'Отелей должно быть <b>не больше 5</b>', reply_markup=button_hotels(),
#                      parse_mode='html')
#     bot.set_state(callback.from_user.id, HighInfo.quantity_result_high)
#
#
# @bot.message_handler(state=HighInfo.quantity_result_high)
# def check_quantity_hotels(message: Message) -> None:
#     number = message.text
#
#     if number.isdigit():
#         if 16 > int(number) > 0:
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['quantity_hotels'] = number
#             bot.send_message(message.chat.id, 'Принято! Осталось самая малость 😁')
#             bot.send_message(message.chat.id, 'Хотите увидеть фотографии для каждого отеля?',
#                              reply_markup=button_photo())
#             bot.set_state(message.from_user.id, HighInfo.photo_high)
#         else:
#             bot.set_state(message.from_user.id, HighInfo.quantity_result_high)
#             bot.send_message(message.chat.id, 'Число должно быть больше 0, но меньше 6\n'
#                                               'Попробуйте еще раз 🤧')
#     else:
#         bot.set_state(message.from_user.id, HighInfo.quantity_result_high)
#         bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
#                                           'Попробуйте еще раз 🤧')
#
#
# @bot.message_handler(state=HighInfo.photo_high)
# def check_photo(message: Message) -> None:
#     if message.text.title().startswith('Да'):
#         bot.send_message(message.chat.id, 'Сколько фотографий хотите увидеть на один отель\n'
#                                           '<b>не больше 4 фотографий, но не меньше двух </b>',
#                          reply_markup=button_quantity_photo(), parse_mode='html')
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['photo'] = True
#         bot.set_state(message.from_user.id, HighInfo.quantity_photo_high)
#
#     elif message.text.title().startswith('Нет'):
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['photo'] = False
#             data['filter'] = "PRICE_HIGHEST_FIRST"
#         calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
#         bot.send_message(message.chat.id, 'Нет, так нет 😕')
#         bot.send_message(message.chat.id, 'Теперь выберите дату заезда', reply_markup=calendar)
#     else:
#         bot.set_state(message.from_user.id, HighInfo.photo_high)
#         bot.send_message(message.chat.id, 'Я вас не понимаю ответ может быть только вида:\n'
#                                           r'Да\Нет, попробуйте еще раз или нажмите кнопку', reply_markup=button_photo())
#
#
# @bot.message_handler(state=HighInfo.quantity_photo_high)
# def check_quantity_photo(message: Message) -> None:
#     number = message.text
#
#     if number.isdigit():
#         if 5 > int(number) > 0:
#             calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['quantity_photo'] = number
#                 data['filter'] = "PRICE_HIGHEST_FIRST"
#             bot.send_message(message.chat.id, 'Теперь выберите дату заезда', reply_markup=calendar)
#         else:
#             bot.set_state(message.from_user.id, HighInfo.quantity_photo_high)
#             bot.send_message(message.chat.id, 'Число должно быть больше 0, но меньше 4\n'
#                                               'Попробуйте еще раз 🤧')
#     else:
#         bot.set_state(message.from_user.id, HighInfo.quantity_photo_high)
#         bot.send_message(message.chat.id, 'Ответ должен являться только числом\n'
#                                           'Попробуйте еще раз 🤧')
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
# def take_data_high_in(callback) -> None:
#     result, key, step1 = DetailedTelegramCalendar(calendar_id=1).process(callback.data)
#     if not result and key:
#         bot.edit_message_text("Выберите дату заезда{}".format(LSTEP[step1]),
#                               callback.message.chat.id,
#                               callback.message.message_id,
#                               reply_markup=key)
#     elif result:
#         with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
#             data['data_in'] = result
#         bot.edit_message_text("Твой выбор {}".format(result),
#                               callback.message.chat.id,
#                               callback.message.message_id)
#         calendar1, step2 = DetailedTelegramCalendar(calendar_id=2).build()
#         bot.send_message(callback.message.chat.id, 'Теперь выбери дату отъезда', reply_markup=calendar1)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
# def take_data_high_out(callback) -> None:
#     result, key, step = DetailedTelegramCalendar(calendar_id=2).process(callback.data)
#     if not result and key:
#         bot.edit_message_text("Выберите дату отъезда{}".format(LSTEP[step]),
#                               callback.message.chat.id,
#                               callback.message.message_id,
#                               reply_markup=key)
#     elif result:
#         with bot.retrieve_data(callback.from_user.id, callback.message.chat.id) as data:
#             data['data_out'] = result
#         bot.edit_message_text("Твой выбор {}".format(result),
#                               callback.message.chat.id,
#                               callback.message.message_id)
#         bot.delete_state(callback.from_user.id, callback.message.chat.id)
#
#         bot.send_message(callback.message.chat.id, 'Cупер, сейчас покажу отели, которые тебе подойдут!')
#         querystring = {"destinationId": data['city_id'],
#                        "pageNumber": "1", "pageSize": data['quantity_hotels'],
#                        "checkIn": str(data['data_in']), "checkOut": str(data['data_out']),
#                        "adults1": "1", "sortOrder": data['filter'], "locale": "en_US",
#                        "currency": "USD"}
#
#         hotels = found_hotels(querystring=querystring)
#
#         for hotel in hotels:
#             if data['photo']:
#                 bot.send_media_group(callback.message.chat.id, take_photo(hotel['hotel_id'],
#                                                                           data['quantity_photo']))
#             bot.send_message(callback.message.chat.id, '📝 Название отеля: {name}\n'
#                                                        '🚕 Адреc: {address}\n'
#                                                        '👣 Расстояние до центра: {center}\n'
#                                                        '💸 Цена за ночь:{price}\n'
#                                                        '💰 {total_price}'.format(
#                                                         name=hotel['hotel_name'], address=hotel['address'],
#                                                         center=hotel['center_distance'], price=hotel['price'],
#                                                         total_price=hotel['total_price']),
#                              reply_markup=url_markup(hotel['url']))
