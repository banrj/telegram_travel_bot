from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start', 'hello'])
def bot_start(message: Message):
    """
    Функция приветствия, и начла работы бота.
    :param message: сообщение пользователя
    """
    bot.reply_to(message, "Привет, {name}! Я помогу найти отель, который тебе идеально подойдет."
                          "чтобы узнать ,что я могу можно ввести команду /help".format(
                            name=message.from_user.full_name))

