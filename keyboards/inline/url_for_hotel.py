from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def url_markup(url: str) -> InlineKeyboardMarkup:
    """
    Получает ссылку на отель и превращает ее в кнопку.
    :param url: ссылка отеля.
    :return: инлайн кнопку для перехода на страницу отеля
    """
    mark = InlineKeyboardMarkup()
    mark.add(InlineKeyboardButton(text='Перейти на страницу отеля', url=url))

    return mark
