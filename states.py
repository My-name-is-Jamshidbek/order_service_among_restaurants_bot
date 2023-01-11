from aiogram.dispatcher.filters.state import State, StatesGroup

class states_order_food(StatesGroup):
    restaurant_name = State()
    menu = State()
    type_table = State()
    phone_number = State()

class states_order_table(StatesGroup):
    restaurant_name = State()
    type_table = State()
    phone_number = State()

class states_order_delivery(StatesGroup):
    restaurant_name = State()
    menu = State()
    type_table = State()
    phone_number = State()
    location = State()