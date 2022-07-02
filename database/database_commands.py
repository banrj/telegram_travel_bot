from database.models import Command, Result, Request, db, CharField
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from loguru import logger
from loader import bot
from telebot.types import Message


def check_database() -> None:
    """
    Функция проверяет наличие базы данных, если БД не существует, то создает её.
    В конце создает таблицы.
    """
    logger.add('debug_in_database.log', level='DEBUG', format="{time} {level} {message}", rotation="10 KB",
               compression="zip")
    con = psycopg2.connect("user='postgres' host='localhost' password='12345'")
    dbname = 'history'

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute('CREATE DATABASE ' + dbname)
        logger.info('DATABASE created')

    except psycopg2.ProgrammingError as err:
        logger.exception(err)
        logger.error('DATABASE already exists')

    finally:
        with db:
            db.create_tables([Request, Command, Result])


def insert_in_requests(user_id: int, time: datetime) -> int:
    """
    Cоздаёт запись в таблице requests
    :param user_id: id пользователя
    :param time: время когда пользователь сделал запрос
    :return: айди записи для создания связи между таблицами
    """
    with db:
        request = Request.create(user_id=user_id, time=time)
        logger.info('INSERT in requests')
    return request.id


def insert_in_commands(request_id, command_name: str, city_name: str,
                       data_in: str, data_out: str, quantity: str,
                       min_price: CharField = None, max_price: CharField = None, min_distance: CharField = None,
                       max_distance: CharField = None) -> int:
    """
    Cоздаёт запись в таблице commands
    :param request_id: айди прошлого запроса(requests)
    :param command_name: имя команды
    :param city_name: названия города
    :param data_in: дата заезда
    :param data_out: дата выезда
    :param quantity: кол-во отелей
    :param min_price: мин. цена (optional)
    :param max_price: макс. цена (optional)
    :param min_distance: мин. дистанция до центра (optional)
    :param max_distance: макс. дистанция до центра (optional)
    :return: айди записи для создания связи между таблицами
    """
    with db:
        command = Command.create(request_id=request_id, command_name=command_name, city_name=city_name,
                                 min_price=min_price, max_price=max_price, min_distance=min_distance,
                                 max_distance=max_distance, data_in=data_in, data_out=data_out, quantity=quantity)
        logger.info('INSERT in commands')
    return command.id


def insert_in_results(command_id, hotel: str, address: str, price: str,
                      distance: str, total_price: str, url: str) -> None:
    """
    Cоздаёт запись в таблице results
    :param command_id: айди прошлого запроса(commands)
    :param hotel: название отеля
    :param address: адрес
    :param price: цена за ночь
    :param distance: расстояние до центра
    :param total_price: общая сумма денег
    :param url: ссылка на отель
    :return: None
    """
    with db:
        Result.insert(command_id=command_id, hotel=hotel, address=address, price=price,
                      distance=distance, total_price=total_price, url=url).execute()
        logger.info('INSERT in results')


@logger.catch()
def select_user_history(message: Message):
    """
    Получает из базы данных историю всех запросов пользователя лимит(5),
    после этого обрабатывает их и приводит в тип текста.
    И после всего этого выводит пользователю его команду и отели которые он нашел, с помощью этой команды.
    :param message: сообщение пользователя(с помощью него мы получаем id,
    и имеем возможность отправить текст из функции)
    """
    with db:
        keys = Request.select().where(Request.user_id == message.from_user.id).limit(5).order_by(Request.time.desc())
        for key in keys:
            command = Command.select().where(Command.request_id == key).get()
            text1 = (f'Время: {str(key.time)[0:19]}  Команда: {command.command_name}\n'
                     f'Город: {command.city_name}, с {command.data_in} по {command.data_out}')
            if command.command_name == 'beastdeal':
                text1 += (f'параметры поиска:\n'
                          f'минимальная цена: {command.min_price} и максимальная цена: {command.max_price}\n'
                          f'минимальное расстояние: {command.min_distance}'
                          f' и максимальное расстояние: {command.max_distance}\n')
            bot.send_message(message.chat.id, text1)

            history = Result.select().where(Result.command_id == key)
            for one_story in history:
                text2 = (f'Название отеля: {one_story.hotel}, цена за ночь: {one_story.price}\n'
                         f'Расстояние до центра {one_story.distance}\n'
                         f'Полная стоимость проживания {one_story.total_price}\n'
                         f'Адресс: {one_story.address}\nСсылка на страницу отеля: {one_story.url}')

                bot.send_message(message.chat.id, text2, disable_web_page_preview=True)



