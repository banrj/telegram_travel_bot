from utils.misc.locations_request import found_cities
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional


def city_markup(name) -> Optional[InlineKeyboardMarkup]:
    """
    Создает список из инлайн кнопок с городами, которые совпали с названием города, которе получила функция.
    :param name: названия города.
    :return: возвращает список городов, города являются инлайн кнопками
    """
    cities = found_cities(city_name=name)
    destinations = InlineKeyboardMarkup()
    if not cities:
        return
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data='city_id{}'.format(
            city["destination_id"])))
    return destinations

