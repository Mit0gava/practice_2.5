import sqlite3

# Подключение
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Таблица
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    patronymic TEXT,
    group_name TEXT,
    grades TEXT
)
""")
conn.commit()


# Добавление
def add_student():
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество: ")
    group = input("Группа: ")

    grades = []
    for i in range(4):
        grades.append(int(input(f"Оценка {i+1}: ")))

    cursor.execute(
        "INSERT INTO students VALUES (NULL,?,?,?,?,?)",
        (name, surname, patronymic, group, str(grades))
    )
    conn.commit()


# Все студенты
def show_all():
    for row in cursor.execute("SELECT * FROM students"):
        print(row)


# Один студент
def show_one():
    student_id = input("ID: ")

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cursor.fetchone()

    if row:
        grades = eval(row[5])
        avg = sum(grades) / len(grades)

        print(row)
        print("Средний балл:", avg)
    else:
        print("Не найден")


# Редактирование
def edit_student():
    student_id = input("ID: ")
    name = input("Новое имя: ")

    cursor.execute("UPDATE students SET name=? WHERE id=?", (name, student_id))
    conn.commit()


# Удаление
def delete_student():
    student_id = input("ID: ")
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


# Средний по группе
def group_avg():
    group = input("Группа: ")

    cursor.execute("SELECT grades FROM students WHERE group_name=?", (group,))
    rows = cursor.fetchall()

    all_grades = []

    for row in rows:
        all_grades += eval(row[0])

    if all_grades:
        print("Средний балл группы:", sum(all_grades)/len(all_grades))
    else:
        print("Нет данных")


# Меню
while True:
    print("\n1 Добавить")
    print("2 Показать всех")
    print("3 Показать одного")
    print("4 Редактировать")
    print("5 Удалить")
    print("6 Средний по группе")
    print("7 Выход")

    c = input("Выбор: ")

    if c == "1":
        add_student()
    elif c == "2":
        show_all()
    elif c == "3":
        show_one()
    elif c == "4":
        edit_student()
    elif c == "5":
        delete_student()
    elif c == "6":
        group_avg()
    elif c == "7":
        break