from telebot.types import Message
from database.database_commands import check_database
from loader import bot


@bot.message_handler(commands=['start', 'hello'])
def bot_start(message: Message):
    """
    Функция приветствия, и начала работы бота.
    Плюс функция вызывает функцию проверки БД.
    :param message: сообщение пользователя
    """
    check_database()
    bot.reply_to(message, "Привет, {name}! Я помогу найти отель, который тебе идеально подойдет."
                          "чтобы узнать ,что я могу можно ввести команду /help".format(
                            name=message.from_user.full_name))

