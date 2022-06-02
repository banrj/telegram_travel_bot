from telebot.handler_backends import State, StatesGroup


class Info(StatesGroup):
    city = State()
    quantity_result = State()
    photo = State()
    quantity_photo = State()


class BestInfo(StatesGroup):
    city = State()
    quantity_result = State()
    photo = State()
    quantity_photo = State()
    price = State()     # for beast_deal
    distance_to_center = State()    # for beast_deal
