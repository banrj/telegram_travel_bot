from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Эхо хендлер, куда летят текстовые сообщения без указанного состояния.
    :param message: сообщение пользователя
    """
    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:{message}".format(message=message.text))

