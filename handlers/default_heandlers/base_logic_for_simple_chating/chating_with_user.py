from loader import bot
from telebot.types import Message
from typing import List
import random


@bot.message_handler(content_types=['text'])
def logic(message: Message) -> None:
    simple_welcome_en: List[str] = ['Hi', 'Hello', 'Hey']
    simple_welcome_ru: List[str] = ['Привет', 'Здравствуй', 'Здравствуйте', 'Добро пожаловать']
    if message.text.title() in simple_welcome_en:
        bot.send_message(message.chat.id, '{welcome} {name}'.format(welcome=random.choice(simple_welcome_en),
                                                                    name=message.from_user.full_name))
    elif message.text.title() in simple_welcome_ru:
        bot.send_message(message.chat.id, '{welcome} {name}'.format(welcome=random.choice(simple_welcome_ru),
                                                                    name=message.from_user.full_name))
    else:
        bot.send_message(message.chat.id, '{name} прости я тебя не понимаю'.format(name=message.from_user.full_name))
