from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from config import *
from buttons import *
from database import *
from states import *



bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#START
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, "Welcome to the restaurant ordering bot! Please choose an option:", reply_markup=buttons_get_menu_keyboard())

#MAIN MENU
@dp.message_handler()
async def handle_text(message: types.Message):
    if message.text.lower() == "Order food".lower():
        await bot.send_message(message.chat.id, f"Please select a restaurant:",reply_markup=buttons_get_restaurant_keyboard())
        await states_order_food.restaurant_name.set()
    elif message.text.lower() == "Order table".lower():
        await bot.send_message(message.chat.id, "Please select a restaurant:",reply_markup=buttons_get_restaurant_keyboard())
        await states_order_table.restaurant_name.set()
    elif message.text.lower() == "Order delivery".lower():
        await bot.send_message(message.chat.id, "Please select a restaurant:", reply_markup=buttons_get_restaurant_keyboard())
        await states_order_delivery.restaurant_name.set()


#ORDER FOOD
@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_food.restaurant_name)
async def f11(message:types.Message,state:FSMContext):
    if message.text == "Close":
        await message.answer("Closed:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        restaurant_name = message.text
        if not database_check_restaurant_exist(restaurant_name):
            await message.answer("Invalid restaurant. Please select a valid restaurant:",
                                 reply_markup=buttons_get_restaurant_keyboard())
        else:
            await message.answer("You selected {}. Please choose a menu::".format(restaurant_name),
                                 reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
            await state.update_data(restaurant_name=restaurant_name)
            await states_order_food.menu.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state = states_order_food.menu)
async def f10(message:types.Message,state:FSMContext):
    if message.text == "Close":
        await message.answer("Closed:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        menu = message.text
        data = await state.get_data()
        restaurant_name = data.get("restaurant_name")
        if not database_check_menu_exist(restaurant_name, menu):
            await message.answer("Invalid menu. Please choose a valid menu:",
                                 reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
        else:
            await message.answer("You ordered {} from {} restaurant. Choose table type:".format(menu, restaurant_name),reply_markup=buttons_get_table_type_keyboard())
            await state.update_data(menu=menu)
            await states_order_food.type_table.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_food.type_table)
async def f9(message:types.Message,state:FSMContext):
    if message.text == "Close":
        await message.answer("Closed:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        if message.text in ["1 person","2 persons","Family"]:
            await message.answer("Please enter a phone number:",reply_markup=buttons_get_phone_number_keyboard())
            await state.update_data(type_table = message.text)
            await states_order_food.phone_number.set()
        else:
            await message.answer("Table type is incorrect!!!")
@dp.message_handler(content_types=types.ContentType.CONTACT,state=states_order_food.phone_number)
async def f8(message:types.Message,state:FSMContext):
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    table_type = data.get("type_table")
    menu = data.get("menu")
    phone_number = message.contact.phone_number
    full_name = message.contact.full_name
    user_id = message.contact.user_id
    await bot.send_message(ADMIN_ID,f"Ordered food:\nRestaurant name: {restaurant_name}\nTable type: {table_type}\nFood: {menu}\nPhone number: {phone_number}\nFull name: {full_name}\nUser id: {user_id}")
    await message.answer("Ordered food.",reply_markup=buttons_get_menu_keyboard())
    await state.finish()

#ORDER DEILIVERY
@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_delivery.restaurant_name)
async def f7(message:types.Message,state:FSMContext):
    if message.text == "Close":
        await message.answer("Closed:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        restaurant_name = message.text
        if not database_check_restaurant_exist(restaurant_name):
            await message.answer("Invalid restaurant. Please select a valid restaurant:",
                                 reply_markup=buttons_get_restaurant_keyboard())
        else:
            await message.answer("You selected {}. Please choose a menu:".format(restaurant_name),
                                 reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
            await state.update_data(restaurant_name=restaurant_name)
            await states_order_delivery.menu.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state = states_order_delivery.menu)
async def f6(message:types.Message,state:FSMContext):
    menu = message.text
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    if not database_check_menu_exist(restaurant_name, menu):
        await message.answer("Invalid menu. Please choose a valid menu:",
                             reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
    else:
        await message.answer("You ordered {} from {} restaurant. Please send location:".format(menu,restaurant_name),reply_markup=buttons_get_location_keyboard())
        await state.update_data(menu=menu)
        await states_order_delivery.location.set()

@dp.message_handler(content_types=types.ContentType.LOCATION,state=states_order_delivery.location)
async def f5(message:types.Message,state:FSMContext):
    await message.answer("Please enter a phone number:",reply_markup=buttons_get_phone_number_keyboard())
    await state.update_data(location = message.location)
    await states_order_delivery.phone_number.set()

@dp.message_handler(content_types=types.ContentType.CONTACT,state=states_order_delivery.phone_number)
async def f4(message:types.Message,state:FSMContext):
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    location = data.get("location")
    menu = data.get("menu")
    phone_number = message.contact.phone_number
    full_name = message.contact.full_name
    user_id = message.contact.user_id
    await bot.send_message(ADMIN_ID,f"Ordered delivery:\nRestaurant name: {restaurant_name}\nFood: {menu}\nPhone number: {phone_number}\nFull name: {full_name}\nUser id: {user_id}")
    await bot.send_location(ADMIN_ID,latitude=location['latitude'],longitude=location['longitude'])
    await message.answer("Ordered delivery.",reply_markup=buttons_get_menu_keyboard())
    await state.finish()

#ORDER TABLE
@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_table.restaurant_name)
async def f3(message:types.Message,state:FSMContext):
    if message.text == "Close":
        await message.answer("Closed:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        restaurant_name = message.text
        if not database_check_restaurant_exist(restaurant_name):
            await message.answer("Invalid restaurant. Please select a valid restaurant:",
                                 reply_markup=buttons_get_restaurant_keyboard())
        else:
            await message.answer("You selected {}. Please choose a table type::".format(restaurant_name),
                                 reply_markup=buttons_get_table_type_keyboard())
            await state.update_data(restaurant_name=restaurant_name)
            await states_order_table.type_table.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_table.type_table)
async def f2(message:types.Message,state:FSMContext):
    if message.text == "Close":
        await message.answer("Closed:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        if message.text in ["1 person","2 persons","Family"]:
            await message.answer("Please enter a phone number:",reply_markup=buttons_get_phone_number_keyboard())
            await state.update_data(type_table = message.text)
            await states_order_table.phone_number.set()
        else:
            await message.answer("Table type is incorrect!!!")
@dp.message_handler(content_types=types.ContentType.CONTACT,state=states_order_table.phone_number)
async def f1(message:types.Message,state:FSMContext):
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    table_type = data.get("type_table")
    phone_number = message.contact.phone_number
    full_name = message.contact.full_name
    user_id = message.contact.user_id
    await bot.send_message(ADMIN_ID,f"Ordered food:\nRestaurant name: {restaurant_name}\nTable type: {table_type}\nPhone number: {phone_number}\nFull name: {full_name}\nUser id: {user_id}")
    await message.answer("Ordered table.",reply_markup=buttons_get_menu_keyboard())
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp)