from utils.misc.locations_request import found_cities
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional


def city_markup(name) -> Optional[InlineKeyboardMarkup]:
    cities = found_cities(city_name=name)
    destinations = InlineKeyboardMarkup()
    if not cities:
        return
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data='city_id{}'.format(
            city["destination_id"])))
    return destinations


def city_markup_high(name) -> Optional[InlineKeyboardMarkup]:
    cities = found_cities(city_name=name)
    destinations = InlineKeyboardMarkup()
    if not cities:
        return
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data='Hcity_id{}'.format(
            city["destination_id"])))
    return destinations



