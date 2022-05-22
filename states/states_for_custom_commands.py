from telebot.handler_backends import State, StatesGroup


class TravelInfo(StatesGroup):
    city = State()
    quantity_result = State()
    price = State()     # for beast_deal
    distance_to_center = State()    # for beast_deal
    photo = State()
    quantity_photo = State()


