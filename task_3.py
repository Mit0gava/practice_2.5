import sqlite3

conn = sqlite3.connect("currency.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT,
    codes TEXT
)
""")
conn.commit()


def add_group():
    name = input("Название группы: ")
    codes = input("Коды валют (через запятую): ")

    cursor.execute("INSERT INTO groups VALUES(NULL,?,?)", (name, codes))
    conn.commit()


def show_groups():
    for row in cursor.execute("SELECT * FROM groups"):
        print(row)


while True:
    print("\n1 Добавить группу")
    print("2 Показать группы")
    print("3 Выход")

    c = input()

    if c == "1":
        add_group()
    elif c == "2":
        show_groups()
    elif c == "3":
        break