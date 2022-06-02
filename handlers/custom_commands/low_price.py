from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['lowprice'])
def answer_low_price(message: Message) -> None:
    bot.send_message(message.chat.id, 'Команда еще не готова')
    bot.send_message(message.chat.id, 'Команда еще не готова')