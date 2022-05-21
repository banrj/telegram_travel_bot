from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['history'])
def answer_history(message: Message) -> None:
    bot.send_message(message.chat.id, 'Команда еще не готова')
