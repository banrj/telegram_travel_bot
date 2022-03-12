from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':

    @bot.message_handler(commands=['start', 'hello-world'])
    def start_answer(message):
        bot.send_message(message.chat.id, "Привет это бот для путешествий чтобы узнать обо мне введи команду /help")


    @bot.message_handler(commands=['help'])
    def help_answer(message):
        bot.send_message(message.chat.id, 'Список команд')

    @bot.message_handler()
    def get_user_text(message):
        if message.text.title() == 'Hello' or message.text.title() == 'Привет':
            bot.send_message(message.chat.id, 'Привет {name}'.format(name=message.from_user.first_name))
        else:
            bot.send_message(message.chat.id, 'Я тебя не понимаю')


bot.infinity_polling()
