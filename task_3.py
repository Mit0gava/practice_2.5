import requests
import sqlite3

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
DB_FILE = "groups.db"

# Создание базы данных и таблицы, если их нет
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS group_currencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    currency_code TEXT,
    FOREIGN KEY(group_id) REFERENCES groups(id)
)
""")
conn.commit()


def get_rates():
    data = requests.get(URL).json()
    return data["Valute"]


def create_group(name):
    try:
        cursor.execute("INSERT INTO groups (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Группа '{name}' создана.")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print("Группа с таким названием уже существует.")
        return None


def add_currency_to_group(group_id, code):
    cursor.execute(
        "INSERT INTO group_currencies (group_id, currency_code) VALUES (?, ?)",
        (group_id, code)
    )
    conn.commit()


def remove_currency_from_group(group_id, code):
    cursor.execute(
        "DELETE FROM group_currencies WHERE group_id=? AND currency_code=?",
        (group_id, code)
    )
    conn.commit()


def get_groups():
    cursor.execute("SELECT id, name FROM groups")
    return cursor.fetchall()


def get_group_currencies(group_id):
    cursor.execute(
        "SELECT currency_code FROM group_currencies WHERE group_id=?",
        (group_id,)
    )
    return [row[0] for row in cursor.fetchall()]


while True:
    print("\n1 Показать все валюты")
    print("2 Найти валюту по коду")
    print("3 Создать группу")
    print("4 Показать группы")
    print("5 Изменить группу")
    print("6 Выход")

    choice = input("Выбор: ")
    rates = get_rates()

    if choice == "1":
        for code in rates:
            print(code, "-", rates[code]["Value"])

    elif choice == "2":
        code = input("Введите код валюты: ").upper()
        if code in rates:
            print(code, "-", rates[code]["Value"])
        else:
            print("Валюта не найдена")

    elif choice == "3":
        name = input("Название группы: ")
        group_id = create_group(name)
        if group_id:
            while True:
                code = input("Добавить валюту (или stop): ").upper()
                if code == "STOP":
                    break
                add_currency_to_group(group_id, code)

    elif choice == "4":
        groups = get_groups()
        for g_id, g_name in groups:
            currencies = get_group_currencies(g_id)
            print(f"{g_name}: {currencies}")

    elif choice == "5":
        name = input("Название группы: ")
        cursor.execute("SELECT id FROM groups WHERE name=?", (name,))
        result = cursor.fetchone()
        if result:
            group_id = result[0]
            print("1 Добавить валюту")
            print("2 Удалить валюту")
            c = input("Выбор: ")

            if c == "1":
                code = input("Код валюты: ").upper()
                add_currency_to_group(group_id, code)

            elif c == "2":
                code = input("Код валюты: ").upper()
                remove_currency_from_group(group_id, code)
        else:
            print("Группа не найдена")

    elif choice == "6":
        break

conn.close()