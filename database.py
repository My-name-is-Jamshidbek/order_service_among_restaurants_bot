import sqlite3


def database_add_restaurant(name, info, location):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO restaurants (name, info, location) VALUES (?,?,?)", (name, info, location))
        con.commit()


def database_delete_restaurant(name):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM restaurants WHERE name = ?", (name,))
        con.commit()


def database_add_menu(restaurant_name, menu_name, price):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO menu (restaurant_name, name, price) VALUES (?,?,?)", (restaurant_name, menu_name, price))
        con.commit()


def database_delete_menu(restaurant_name, menu_name):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM menu WHERE restaurant_name = ? AND name = ?", (restaurant_name, menu_name))
        con.commit()


def database_get_menu(restaurant_name):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("SELECT name, price,restaurant_name FROM menu WHERE restaurant_name = ?", (restaurant_name,))
        f = cur.fetchall()
        cur.close()
    return f


def database_order_table(phone_number, table_type, restaurant_name):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders_table (phone, table_type, restaurant_name) VALUES (?,?,?)", (phone_number, table_type, restaurant_name))
        con.commit()


def database_order_food(phone_number, food, restaurant_name, table_type, menu_numbers, price):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders_food (phone, menu, restaurant_name, table_type, menu_numbers, price) VALUES (?,?,?,?)", (phone_number, food, restaurant_name, table_type, menu_numbers, price))
        con.commit()


def database_order_delivery(phone_number, address, food, restaurant_name, table_type, menu_numbers, price):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders_delivery (phone_number, location, menu, restaurant_name, table_type, menu_numbers, price) VALUES (?,?,?,?,?,?,?)", (phone_number, address, food, restaurant_name, table_type, menu_numbers, price))

        con.commit()


def database_get_restaurants():
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("SELECT name, info, location FROM restaurants")
        return cur.fetchall()


def database_check_menu_exist(restaurant_name,menu_name):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu WHERE restaurant_name=? AND name=?", (restaurant_name,menu_name))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return False
    else:
        return True


def database_check_restaurant_exist(restaurant_name):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurants WHERE name=?", (restaurant_name,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return False
    else:
        return True


def database_menu_price(restaurant_name,menu_name):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM menu WHERE restaurant_name=? AND name=?", (restaurant_name,menu_name))
    data = cursor.fetchone()
    conn.close()
    return data


def database_menu_prices(restaurant_name):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, price FROM menu WHERE restaurant_name=?", (restaurant_name, ))
    data1 = cursor.fetchall()
    conn.close()
    data = ""
    for i in data1:data+=f"{i[0]} : {i[1]} so'm.\n"
    return data


def database_update_price(new_price):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE prices SET price = ?''', (new_price,))

    conn.commit()
    conn.close()


def database_get_current_price():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT price FROM prices''')
    current_price = cursor.fetchone()[0]

    conn.close()
    return current_price


def database_insert_price(new_price):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO prices (price) VALUES (?)''', (new_price,))

    conn.commit()
    conn.close()

def database_delete_all_restaurant_info(restaurant_name):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()

        # Delete all menu items for the restaurant
        cur.execute("DELETE FROM menu WHERE restaurant_name = ?", (restaurant_name,))

        # Delete all table and food orders for the restaurant
        cur.execute("DELETE FROM orders_table WHERE restaurant_name = ?", (restaurant_name,))
        cur.execute("DELETE FROM orders_food WHERE restaurant_name = ?", (restaurant_name,))
        cur.execute("DELETE FROM orders_delivery WHERE restaurant_name = ?", (restaurant_name,))

        # Delete the restaurant's information
        cur.execute("DELETE FROM restaurants WHERE name = ?", (restaurant_name,))

        con.commit()

def create_tables():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS restaurants (name TEXT, info TEXT, location TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (restaurant_name TEXT, name TEXT, price INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_food (id INTEGER PRIMARY KEY,phone TEXT, table_type TEXT, menu TEXT, menu_numbers INTEGER, price INTEGER, restaurant_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_table (id INTEGER PRIMARY KEY,phone TEXT, table_type TEXT, restaurant_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_delivery (id INTEGER PRIMARY KEY,phone_number TEXT, table_type TEXT, menu TEXT, location TEXT,restaurant_name TEXT, menu_numbers INTEGER, price INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS prices (id INTEGER PRIMARY KEY, price REAL)''')
    database_insert_price(1)
    conn.commit()
    conn.close()
# create_tables()
# database_add_restaurant("Baxrom xot-dog","tez tayyorlanadigan taomlar","tatu urganch filiali")
# database_add_menu("Baxrom xot-dog","katta xot-dog",'23000')

