from loader import bot
from telebot.types import Message
from states.states_for_custom_commands import TravelInfo
from utils.API import request_to_api


@bot.message_handler(commands=['lowprice'])
def answer_low_price(message: Message) -> None:
    bot.set_state(message.from_user.id, TravelInfo.city)
    bot.send_message(message.chat.id, 'Напишите в каком городе планируйте найти отель', )


@bot.message_handler(state=TravelInfo.city)
def choice_city(message: Message) -> None:
    if message.text.isalpha():
        text = request_to_api(url="https://hotels4.p.rapidapi.com/locations/v2/search", query=message.text)
        variants_city = text['suggestions']

        bot.send_message(message.from_user.id, '\n'.join(variants_city))

    else:
        bot.send_message(message.chat.id, 'Ошибка название города состоит только из букв\n'
                                          'Напишите в каком городе планируйте найти отель', )

