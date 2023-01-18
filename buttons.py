from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import *

buttons_close_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn = KeyboardButton("Chiqish")
buttons_close_keyboard.add(btn)

def buttons_get_location_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton("Joylashuvni jo'natish",request_location=True)
    keyboard.add(btn)
    return keyboard

def buttons_get_restaurant_keyboard(admin = False):
    restaurants = database_get_restaurants()  # get the list of all the restaurants
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(r[0]) for r in restaurants]
    keyboard.add(*buttons)
    btn = KeyboardButton("Chiqish")
    keyboard.add(btn)
    if admin:keyboard.add("Restaran qo'shish")
    return keyboard

def buttons_get_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    food_button = KeyboardButton("Ovqat buyurtma")
    table_button = KeyboardButton("Stul buyurtma")
    delivery_button = KeyboardButton("Taom yetkazib berish")
    keyboard.add(food_button, table_button, delivery_button)
    return keyboard

def buttons_get_restaurant_menu_keyboard(restaurant_name,admin=False):
    menu = database_get_menu(restaurant_name)  # get the list of the menus for the selected restaurant
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(m[0]) for m in menu]
    keyboard.add(*buttons)
    btn = KeyboardButton("Chiqish")
    keyboard.add(btn)
    if admin:
        keyboard.add("Restaranni o'chirish")
        keyboard.add("Yangi menyu qo'shish")
    return keyboard

def buttons_get_table_type_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    table_type_1 = KeyboardButton("1 odam")
    table_type_2 = KeyboardButton("2 odamlar")
    table_type_3 = KeyboardButton("Oilaviy")
    keyboard.add(table_type_1, table_type_2, table_type_3)
    btn = KeyboardButton("Chiqish")
    keyboard.add(btn)
    return keyboard

def buttons_get_phone_number_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_button = KeyboardButton("Telefon raqamni jo'natish", request_contact=True)
    keyboard.add(phone_button)
    return keyboard

def buttons_get_tasdiqlash():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in ['Tasdiqlash',"Chiqish"]:keyboard.add(i)
    return keyboard


def buttons_admin_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in ['Restaranlar',"Yetkazib berish"]:keyboard.add(i)
    return keyboard


def buttons_(buttons):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in buttons:keyboard.add(i)
    return keyboard


