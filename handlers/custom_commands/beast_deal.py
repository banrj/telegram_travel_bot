from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['beastdeal'])
def answer_beast_deal(message: Message) -> None:
    bot.send_message(message.chat.id, 'Команда еще не готова')
