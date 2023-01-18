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
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin kerakli menyuni tanlang", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    else:await bot.send_message(message.chat.id, "Salom bizning mehmonhona bo'timizga hush kelibsiz. Kerakli bo'limni tanlashingiz mumkin:", reply_markup=buttons_get_menu_keyboard())

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
            await message.answer(text=database_menu_prices(restaurant_name))
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
            await message.answer("Siz {} menyusini {} restaranidagi tanladingiz. Iltimos ovqat nechi kishi uchunligini kiriting:".format(menu, restaurant_name), reply_markup=buttons_close_keyboard)
            await state.update_data(menu=menu)
            await states_order_food.menu_numbers.set()

@dp.message_handler(state=states_order_food.menu_numbers, content_types=types.ContentType.TEXT)
async def f12(m:types.Message, state:FSMContext):
    if m.text == "Chiqish":
            await m.answer("Chiqildi:",reply_markup=buttons_get_menu_keyboard())
            await state.finish()
    elif m.text.isdigit():
        await state.update_data(menu_numbers=m.text)
        await m.answer("Iltimos stol turini tanlang:",reply_markup=buttons_get_table_type_keyboard())
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
    menu_numbers = data.get("menu_numbers")
    price = int(database_menu_price(restaurant_name,menu)[0])*int(menu_numbers)
    await state.update_data(zakas = f"Ovqatga buyurtma:\nRestauran nomi: {restaurant_name}\nstol turi: {table_type}\novqat: {menu}\nOvqatlar soni: {menu_numbers}\nTelefon raqami: {phone_number}\nTo'liq ism: {full_name}\nUser id: {user_id}\nUmmumiy narx: {price} so'm")
    await message.answer(f"Ovqatga buyurtma:\nRestauran nomi: {restaurant_name}\nstol turi: {table_type}\novqat: {menu}\nOvqatlar soni: {menu_numbers}\nTelefon raqami: {phone_number}\nTo'liq ism: {full_name}\nUser id: {user_id}\nUmmumiy narx: {price} so'm",reply_markup=buttons_get_tasdiqlash())
    await states_order_food.price.set()


@dp.message_handler(state=states_order_food.price, content_types=types.ContentType.TEXT)
async def f12(message:types.Message, state: FSMContext):
    if message.text == "Chiqish":
        await message.answer("Chiqildi:", reply_markup=buttons_get_menu_keyboard())
        await state.finish()
    elif message.text == "Tasdiqlash":
        await message.answer("Buyurtma qabul qilindi.", reply_markup=buttons_get_menu_keyboard())
        data = await state.get_data()
        await bot.send_message(ADMIN_ID, data.get("zakas"))
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
            await message.answer(text=database_menu_prices(restaurant_name))
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
        await message.answer("Siz {} menyusini {} restarandagi tanladingiz. Iltimos ovqat sonini jo'nating:".format(menu,restaurant_name),reply_markup=buttons_close_keyboard)
        await state.update_data(menu=menu)
        await states_order_delivery.menu_numbers.set()


@dp.message_handler(content_types=types.ContentType.TEXT,state = states_order_delivery.menu_numbers)
async def f6(message:types.Message,state:FSMContext):
    menu = message.text
    if message.text.isdigit() == False:
        await message.answer("Son xato! Iltimos butun son kiriting:")
    else:
        await message.answer("Iltimos joylashuvingizni jo'nating:",reply_markup=buttons_get_location_keyboard())
        await state.update_data(menu_numbers=menu)
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
    menu = data.get("menu")
    phone_number = message.contact.phone_number
    full_name = message.contact.full_name
    user_id = message.contact.user_id
    menu_numbers = data.get("menu_numbers")
    price = int(database_menu_price(restaurant_name,menu)[0])*int(menu_numbers)
    price+=database_get_current_price()
    zakas = f"Ovqat yetkazib berish:\nRestaurant name: {restaurant_name}\nOvqat: {menu}\novqatlar soni: {menu_numbers}\nTelefon raqam: {phone_number}\nTo'liq ism: {full_name}\nUser id: {user_id}\nyetkazib berish narxi:{database_get_current_price()}\nummumiy narx: {price}"
    await state.update_data(zakas = zakas)
    await message.answer(zakas, reply_markup=buttons_get_tasdiqlash())
    await states_order_delivery.price.set()


@dp.message_handler(state=states_order_delivery.price, content_types=types.ContentType.TEXT)
async def f13(message:types.Message, state: FSMContext):
    if message.text == "Tasdiqlash":
        data = await state.get_data()
        location = data.get("location")
        zakas = data.get("zakas")
        await bot.send_message(ADMIN_ID,zakas)
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


# admin
@dp.message_handler(state=state_admin_menu.menyu,content_types=types.ContentType.TEXT)
async def admin_menu(m:types.Message,state:FSMContext):
    if m.text == "Yetkazib berish":
        await m.answer(f"Yetkazib berish narxi {database_get_current_price()}", reply_markup=buttons_(['Yangilash',"Orqaga"]))
        await state_admin_menu.yetkazib_berish.set()
    elif m.text == "Restaranlar":
        await m.answer(text="Restaranlar:", reply_markup=buttons_get_restaurant_keyboard(admin=True))
        await state_admin_menu.restaranlar_menu.set()


@dp.message_handler(state=state_admin_menu.restaranlar_menu, content_types=types.ContentType.TEXT)
async def admin_menu_restaranlar(m:types.Message, state:FSMContext):
    if m.text == "Restaran qo'shish":
        await m.answer("Yangi restaran nomini kiriting:",reply_markup=buttons_close_keyboard)
        await state_admin_menu.restaran_qoshish.set()
    elif database_check_restaurant_exist(m.text):
        await state.update_data(restaranlar_menu=m.text)
        await m.answer("Taomlar ro'yxati:", reply_markup=buttons_get_restaurant_menu_keyboard(m.text, admin=True))
        await state_admin_menu.restaran_taomlar.set()
    elif m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()


@dp.message_handler(state=state_admin_menu.restaran_qoshish, content_types=types.ContentType.TEXT)
async def admin_restaran_qoshish(m:types.Message, state:FSMContext):
    if m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    else:
        database_add_restaurant(m.text, "info", "location")
        await m.answer("Yangi restaran qo'shildi.")
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()


@dp.message_handler(state=state_admin_menu.restaran_taomlar, content_types=types.ContentType.TEXT)
async def admin_restaran_taomlar(m:types.Message,state:FSMContext):
    menu = m.text
    data = await state.get_data()
    restaurant_name = data.get("restaranlar_menu")
    if m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    elif m.text == "Yangi menyu qo'shish":
        await m.answer("Yangi menyu nomini kiriting:", reply_markup=buttons_close_keyboard)
        await state_admin_menu.restaran_yangi_taom.set()
    elif m.text == "Restaranni o'chirish":
        database_delete_all_restaurant_info(restaurant_name)
        await m.answer("Restaran o'chirildi.")
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    elif database_check_menu_exist(restaurant_name, menu):
        await state.update_data(menyu = m.text)
        await m.answer(f"siz {restaurant_name} restaranidagi {menu} taomini tanladingiz. Kerakli menyuni tanlang:", reply_markup=buttons_(["Taomni o'chirish", "Chiqish"]))
        await state_admin_menu.restaran_taom_menu.set()


@dp.message_handler(state=state_admin_menu.restaran_yangi_taom, content_types=types.ContentType.TEXT)
async def admin_yangi_taom(m:types.Message, state:FSMContext):
    if m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    else:
        await state.update_data(restaran_yangi_taom = m.text)
        await m.answer("Yangi menyu narxini kiriting:\nmasalan: 100",reply_markup=buttons_close_keyboard)
        await state_admin_menu.restaran_yangi_taom_narhi.set()


@dp.message_handler(state = state_admin_menu.restaran_yangi_taom_narhi, content_types=types.ContentType.TEXT)
async def admin_yangi_taom_narhi(m:types.Message, state:FSMContext):
    if m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    elif m.text.isdigit():
        data = await state.get_data()
        restaran = data.get("restaranlar_menu")
        menyu = data.get("restaran_yangi_taom")
        narxi = int(m.text)
        database_add_menu(restaran,menyu,narxi)
        await m.answer("Yangi taom qo'shildi")
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()


@dp.message_handler(state=state_admin_menu.restaran_taom_menu, content_types=types.ContentType.TEXT)
async def admin_restaran_taom_menu(m:types.Message, state:FSMContext):
    if m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    elif m.text == "Taomni o'chirish":
        data = await state.get_data()
        restaurant_name = data.get("restaranlar_menu")
        menyu = data.get("menyu")
        database_delete_menu(restaurant_name,menyu)
        await m.answer("Taom o'chirildi.")
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()

@dp.message_handler(state=state_admin_menu.yetkazib_berish, content_types=types.ContentType.TEXT)
async def admin_yetkazib_berish(m:types.Message, state:FSMContext):
    if m.text == "Orqaga":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    elif m.text == "Yangilash":
        await m.answer("Yangi narxni kiritishingiz mumkin:",reply_markup=buttons_close_keyboard)
        await state_admin_menu.yetkazib_berish_yangilash.set()


@dp.message_handler(state=state_admin_menu.yetkazib_berish_yangilash, content_types=types.ContentType.TEXT)
async def admin_yetkazib_berish_yangilash(m:types.Message, state:FSMContext):
    if m.text == "Chiqish":
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()
    elif m.text.isdigit():
        database_update_price(int(m.text))
        await m.answer("Narx yangilandi.")
        await m.answer("Asosiy menyu:", reply_markup=buttons_admin_menu())
        await state_admin_menu.menyu.set()

if __name__ == '__main__':
    executor.start_polling(dp)