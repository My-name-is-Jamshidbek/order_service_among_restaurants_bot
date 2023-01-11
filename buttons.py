from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import *

buttons_close_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn = KeyboardButton("Close")
buttons_close_keyboard.add(btn)

def buttons_get_location_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton("Send location",request_location=True)
    keyboard.add(btn)
    return keyboard

def buttons_get_restaurant_keyboard():
    restaurants = database_get_restaurants()  # get the list of all the restaurants
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(r[0]) for r in restaurants]
    keyboard.add(*buttons)
    btn = KeyboardButton("Close")
    keyboard.add(btn)
    return keyboard

def buttons_get_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    food_button = KeyboardButton("Order food")
    table_button = KeyboardButton("Order table")
    delivery_button = KeyboardButton("Order delivery")
    keyboard.add(food_button, table_button, delivery_button)
    return keyboard

def buttons_get_restaurant_menu_keyboard(restaurant_name):
    menu = database_get_menu(restaurant_name)  # get the list of the menus for the selected restaurant
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(m[0]) for m in menu]
    keyboard.add(*buttons)
    btn = KeyboardButton("Close")
    keyboard.add(btn)
    return keyboard

def buttons_get_table_type_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    table_type_1 = KeyboardButton("1 person")
    table_type_2 = KeyboardButton("2 persons")
    table_type_3 = KeyboardButton("Family")
    keyboard.add(table_type_1, table_type_2, table_type_3)
    btn = KeyboardButton("Close")
    keyboard.add(btn)
    return keyboard

def buttons_get_phone_number_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_button = KeyboardButton("Share Phone Number", request_contact=True)
    keyboard.add(phone_button)
    return keyboard