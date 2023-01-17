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
    await bot.send_message(message.chat.id, "Salom bizning mehmonhona bo'timizga hush kelibsiz. Kerakli bo'limni tanlashingiz mumkin:", reply_markup=buttons_get_menu_keyboard())

#MAIN MENU
@dp.message_handler()
async def handle_text(message: types.Message):
    if message.text.lower() == "Ovqat buyurtma".lower():
        await bot.send_message(message.chat.id, f"Iltimos restaranni tanlang:",reply_markup=buttons_get_restaurant_keyboard())
        await states_order_food.restaurant_name.set()
    elif message.text.lower() == "Stul buyurtma".lower():
        await bot.send_message(message.chat.id, "Iltimos restaranni tanlang:",reply_markup=buttons_get_restaurant_keyboard())
        await states_order_table.restaurant_name.set()
    elif message.text.lower() == "Taom yetkazib berish".lower():
        await bot.send_message(message.chat.id, "Iltimos restaranni tanlang:", reply_markup=buttons_get_restaurant_keyboard())
        await states_order_delivery.restaurant_name.set()


#ORDER FOOD
@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_food.restaurant_name)
async def f11(message:types.Message,state:FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        restaurant_name = message.text
        if not database_check_restaurant_exist(restaurant_name):
            await message.answer("Restaran nomi noto'g'ri. Iltimos restaranni tanlang:",
                                 reply_markup=buttons_get_restaurant_keyboard())
        else:
            await message.answer("Siz {} restaranini tanladingiz. Iltimos menyuni tanlang:".format(restaurant_name),
                                 reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
            await state.update_data(restaurant_name=restaurant_name)
            await states_order_food.menu.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state = states_order_food.menu)
async def f10(message:types.Message,state:FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        menu = message.text
        data = await state.get_data()
        restaurant_name = data.get("restaurant_name")
        if not database_check_menu_exist(restaurant_name, menu):
            await message.answer("Menyu noto'g'ri! Iltimos menyuni tanlang:",
                                 reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
        else:
            await message.answer("Siz {} menyusini {} restaranidagi tanladingiz. Iltimos stol turini tanlang:".format(menu, restaurant_name),reply_markup=buttons_get_table_type_keyboard())
            await state.update_data(menu=menu)
            await states_order_food.type_table.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_food.type_table)
async def f9(message:types.Message,state:FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        if message.text in ["1 odam","2 odamlar","Oilaviy"]:
            await message.answer("Iltimos telefon raqamingizni jo'nating:",reply_markup=buttons_get_phone_number_keyboard())
            await state.update_data(type_table = message.text)
            await states_order_food.phone_number.set()
        else:
            await message.answer("Stol turi noto'g'ri!!!")
@dp.message_handler(content_types=types.ContentType.CONTACT,state=states_order_food.phone_number)
async def f8(message:types.Message,state:FSMContext):
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    table_type = data.get("type_table")
    menu = data.get("menu")
    phone_number = message.contact.phone_number
    full_name = message.contact.full_name
    user_id = message.contact.user_id
    await bot.send_message(ADMIN_ID,f"Ovqatga buyurtma:\nRestauran nomi: {restaurant_name}\nstol turi: {table_type}\novqat: {menu}\nTelefon raqami: {phone_number}\nTo'liq ism: {full_name}\nUser id: {user_id}")
    await message.answer("Ovqat buyurtma qilindi.",reply_markup=buttons_get_menu_keyboard())
    await state.finish()

#ORDER DEILIVERY
@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_delivery.restaurant_name)
async def f7(message:types.Message,state:FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        restaurant_name = message.text
        if not database_check_restaurant_exist(restaurant_name):
            await message.answer("Restaran nomi noto'g'ri iltimos restaran nomini tanlang:",
                                 reply_markup=buttons_get_restaurant_keyboard())
        else:
            await message.answer("Siz {} restaranini tanladingiz. Iltimos menyuni tanlang:".format(restaurant_name),
                                 reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
            await state.update_data(restaurant_name=restaurant_name)
            await states_order_delivery.menu.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state = states_order_delivery.menu)
async def f6(message:types.Message,state:FSMContext):
    menu = message.text
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    if not database_check_menu_exist(restaurant_name, menu):
        await message.answer("Menyu xato! Iltimos menyuni tanlang:",
                             reply_markup=buttons_get_restaurant_menu_keyboard(restaurant_name))
    else:
        await message.answer("Siz {} menyusini {} restarandagi tanladingiz. Iltimos joylashuvingizni jo'nating:".format(menu,restaurant_name),reply_markup=buttons_get_location_keyboard())
        await state.update_data(menu=menu)
        await states_order_delivery.location.set()

@dp.message_handler(content_types=types.ContentType.LOCATION,state=states_order_delivery.location)
async def f5(message:types.Message,state:FSMContext):
    await message.answer("Iltimos telefon raqamingizni jo'nating:",reply_markup=buttons_get_phone_number_keyboard())
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
    await bot.send_message(ADMIN_ID,f"Ovqat yetkazib berish:\nRestaurant name: {restaurant_name}\nOvqat: {menu}\nTelefon raqam: {phone_number}\nTo'liq ism: {full_name}\nUser id: {user_id}")
    await bot.send_location(ADMIN_ID,latitude=location['latitude'],longitude=location['longitude'])
    await message.answer("Ovqat yetkazib berishga buyurtma berildi.",reply_markup=buttons_get_menu_keyboard())
    await state.finish()

#ORDER TABLE
@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_table.restaurant_name)
async def f3(message:types.Message,state:FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        restaurant_name = message.text
        if not database_check_restaurant_exist(restaurant_name):
            await message.answer("Restaran nomi noto'g'ri! Iltimos restaran nomini tanlang:",
                                 reply_markup=buttons_get_restaurant_keyboard())
        else:
            await message.answer("Siz {} restaranini tanladingiz Iltimos stol turini tanlang. :".format(restaurant_name),
                                 reply_markup=buttons_get_table_type_keyboard())
            await state.update_data(restaurant_name=restaurant_name)
            await states_order_table.type_table.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state=states_order_table.type_table)
async def f2(message:types.Message,state:FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    else:
        if message.text in ["1 odam","2 odamlar","Oilaviy"]:
            await message.answer("Iltimos telefon raqamingizni jo'nating:",reply_markup=buttons_get_phone_number_keyboard())
            await state.update_data(type_table = message.text)
            await states_order_table.phone_number.set()
        else:
            await message.answer("Stol turi noto'g'ri!!!")
@dp.message_handler(content_types=types.ContentType.CONTACT,state=states_order_table.phone_number)
async def f1(message:types.Message,state:FSMContext):
    data = await state.get_data()
    restaurant_name = data.get("restaurant_name")
    table_type = data.get("type_table")
    phone_number = message.contact.phone_number
    full_name = message.contact.full_name
    user_id = message.contact.user_id
    await bot.send_message(ADMIN_ID,f"Stolga buyurtma:\nRestaurant name: {restaurant_name}\nStol turi: {table_type}\nTelefon raqam: {phone_number}\nTo'liq ism: {full_name}\nUser id: {user_id}")
    await message.answer("Stol buyurtma qilindi.",reply_markup=buttons_get_menu_keyboard())
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp)