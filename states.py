from aiogram.dispatcher.filters.state import State, StatesGroup

class states_order_food(StatesGroup):
    restaurant_name = State()
    menu = State()
    menu_numbers = State()
    price = State()
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
    menu_numbers = State()
    price = State()
    zakas = State()

class state_admin_menu(StatesGroup):
    menyu = State()
    yetkazib_berish = State()
    yetkazib_berish_yangilash = State()
    restaranlar_menu = State()
    restaran_qoshish = State()
    restaran_taomlar = State()
    restaran_yangi_taom = State()
    restaran_taom_menu = State()
    restaran_yangi_taom_narhi = State()