import datetime

from peewee import PostgresqlDatabase, Model, PrimaryKeyField, CharField, DateTimeField, DateField, ForeignKeyField

db = PostgresqlDatabase('history', user='postgres', password='12345', host='localhost', port=5432)


class BaseModel(Model):
    """
    Миксин класс, стандартный для всех других таблиц.
    """
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Request(BaseModel):
    """
    Класс(таблица) запросов.
    """
    user_id = CharField(max_length=50)
    time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        order_by = 'user_id', 'time'
        db_table = 'requests'


class Command(BaseModel):
    """
    Класс(таблица) команд.
    """
    command_name = CharField(max_length=12)
    city_name = CharField(max_length=60)
    min_price = CharField(null=True)
    max_price = CharField(null=True)
    min_distance = CharField(null=True)
    max_distance = CharField(null=True)
    data_in = DateField()
    data_out = DateField()
    quantity = CharField(max_length=1)
    request_id = ForeignKeyField(Request)

    class Meta:
        order_by = 'request_id'
        db_table = 'commands'


class Result(BaseModel):
    """
    Класс(таблица) результатов, который получил пользователь.
    """
    hotel = CharField()
    address = CharField(max_length=100)
    price = CharField(max_length=20)
    distance = CharField(max_length=10)
    total_price = CharField(max_length=70)
    url = CharField(max_length=100)
    command_id = ForeignKeyField(Command)

    class Meta:
        db_table = 'results'

