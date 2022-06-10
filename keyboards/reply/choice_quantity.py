from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_hotels() -> ReplyKeyboardMarkup:
    """
     Создаёт клавиатуру и кнопки с цифрами для выбора кол-во отелей.
     :return: клавиатуру с вариантами нажатия 1 2 3 4 5
     """
    numbers = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    button1 = KeyboardButton(text='1')
    button2 = KeyboardButton(text='2')
    button3 = KeyboardButton(text='3')
    button4 = KeyboardButton(text='4')
    button5 = KeyboardButton(text='5')
    numbers.row(button1, button2, button3, button4, button5)
    return numbers


def button_quantity_photo() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру и кнопки с цифрами для выбора кол-во фоток.
    :return: клавиатуру с вариантами нажатия 2 3 4
    """
    numbers = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    button2 = KeyboardButton(text='2')
    button3 = KeyboardButton(text='3')
    button4 = KeyboardButton(text='4')

    numbers.row(button2, button3, button4)
    return numbers
