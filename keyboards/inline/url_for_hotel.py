from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def url_markup(url: str) -> InlineKeyboardMarkup:
    mark = InlineKeyboardMarkup()
    mark.add(InlineKeyboardButton(text='Перейти на страницу отеля', url=url))

    return mark
