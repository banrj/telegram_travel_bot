from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = ['/{command} - {desk}'.format(desk=desk, command=command) for command, desk in DEFAULT_COMMANDS]

    bot.send_message(message.chat.id, '{phrase}{commands}'.format(phrase='Вот что я могу\n',
                                                                  commands='\n'.join(text)))
