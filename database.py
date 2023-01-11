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

def database_order_food(phone_number, food, restaurant_name, table_type):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders_food (phone, menu, restaurant_name, table_type) VALUES (?,?,?,?)", (phone_number, food, restaurant_name, table_type))
        con.commit()

def database_order_delivery(phone_number, address, food, restaurant_name, table_type):
    with sqlite3.connect('restaurant.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO orders_delivery (phone_number, location, menu, restaurant_name, table_type) VALUES (?,?,?,?,?)", (phone_number, address, food, restaurant_name, table_type))

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


def create_tables():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS restaurants (name TEXT, info TEXT, location TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (restaurant_name TEXT, name TEXT, price INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_food (id INTEGER PRIMARY KEY,phone TEXT, table_type TEXT, menu TEXT, restaurant_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_table (id INTEGER PRIMARY KEY,phone TEXT, table_type TEXT, restaurant_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_delivery (id INTEGER PRIMARY KEY,phone_number TEXT, table_type TEXT, menu TEXT, location TEXT,restaurant_name TEXT)''')

    conn.commit()
    conn.close()
# create_tables()
# database_add_restaurant("Baxrom xot-dog","tez tayyorlanadigan taomlar","tatu urganch filiali")
# database_add_menu("Baxrom xot-dog","loli kabob",'25000')