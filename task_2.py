import sqlite3

conn = sqlite3.connect("drinks.db")
cursor = conn.cursor()

# Таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS drinks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    strength REAL,
    quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cocktails (
    id INTEGER PRIMARY KEY,
    name TEXT,
    composition TEXT,
    price REAL
)
""")

conn.commit()


# Дбавляем напиток
def add_drink():
    name = input("Название: ")
    strength = float(input("Крепость: "))
    qty = int(input("Количество: "))

    cursor.execute("INSERT INTO drinks VALUES(NULL,?,?,?)",
                   (name, strength, qty))
    conn.commit()


# Добавляем коктейль
def add_cocktail():
    name = input("Название: ")
    composition = input("Состав (через запятую): ")
    price = float(input("Цена: "))

    cursor.execute("INSERT INTO cocktails VALUES(NULL,?,?,?)",
                   (name, composition, price))
    conn.commit()


# Продажа
def sell_drink():
    name = input("Что продаем: ")

    cursor.execute("SELECT quantity FROM drinks WHERE name=?", (name,))
    row = cursor.fetchone()

    if row and row[0] > 0:
        cursor.execute("UPDATE drinks SET quantity=quantity-1 WHERE name=?", (name,))
        conn.commit()
        print("Продано")
    else:
        print("Нет в наличии")



def sell_cocktail():
    name = input("Какой коктейль: ")

    cursor.execute("SELECT composition FROM cocktails WHERE name=?", (name,))
    row = cursor.fetchone()

    if not row:
        print("Нет такого коктейля")
        return

    ingredients = row[0].split(",")

    # проверка
    for ing in ingredients:
        cursor.execute("SELECT quantity FROM drinks WHERE name=?", (ing.strip(),))
        check = cursor.fetchone()

        if not check or check[0] <= 0:
            print(f"Не хватает: {ing}")
            return

    # списание
    for ing in ingredients:
        cursor.execute(
            "UPDATE drinks SET quantity = quantity - 1 WHERE name=?",
            (ing.strip(),)
        )

    conn.commit()
    print("Коктейль продан")


# Пополнение
def restock():
    name = input("Напиток: ")
    amount = int(input("Сколько добавить: "))

    cursor.execute("UPDATE drinks SET quantity=quantity+? WHERE name=?", (amount, name))
    conn.commit()


# меню
while True:
    print("\n1 Добавить напиток")
    print("2 Добавить коктейль")
    print("3 Продать напиток")
    print("4 Продать коктейль")
    print("5 Пополнить")
    print("6 Выход")

    c = input("\nВыбор: ")

    if c == "1":
        add_drink()
    elif c == "2":
        add_cocktail()
    elif c == "3":
        sell_drink()
    elif c == "4":
        sell_cocktail()
    elif c == "5":
        restock()
    elif c == "6":
        break