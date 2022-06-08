from telebot.handler_backends import State, StatesGroup


class Info(StatesGroup):
    city = State()
    quantity_result = State()
    photo = State()
    quantity_photo = State()
    min_price = State()  # for beast_deal
    max_price = State()  # for beast_deal
    min_distance_to_center = State()  # for beast_deal
    max_distance_to_center = State()  # for beast_deal
