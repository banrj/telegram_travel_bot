from loader import bot
from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


@bot.message_handler(commands=['beastdeal'])
def answer_beast_deal(message: Message) -> None:
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id, 'Выберите {}'.format(LSTEP[step]), reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def take_data(callback) -> None:
    result, key, step = DetailedTelegramCalendar().process(callback.data)
    if not result and key:
        bot.edit_message_text("Выберите {}".format(LSTEP[step]),
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text("Твой выбор {}".format(result),
                              callback.message.chat.id,
                              callback.message.message_id)
