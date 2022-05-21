from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['highprice'])
def answer_high_price(message: Message) -> None:
    bot.send_message(message.chat.id, 'Команда еще не готова')
