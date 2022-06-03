from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def button_photo() -> ReplyKeyboardMarkup:
    main_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton(text='ДА✅')
    button2 = KeyboardButton(text='НЕТ❌')
    main_button.row(button1, button2)

    return main_button
