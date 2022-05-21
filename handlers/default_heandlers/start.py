from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start', 'hello'])
def bot_start(message: Message):
    bot.reply_to(message, "Привет, {name}!".format(name=message.from_user.full_name))

