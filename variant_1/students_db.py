# --- Часть I, задание 37: CRUD для таблицы students
import sqlite3

DB_PATH = 'students.db'


def init_db():
    # создание таблицы для проверки, по условию она уже есть
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "grade INTEGER)"
        )
        conn.commit()
    finally:
        conn.close()


def add_student(name, grade):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, grade) VALUES (?, ?)",
            (name, grade)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return False
    finally:
        conn.close()


def get_all_students():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, grade FROM students")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append((row['id'], row['name'], row['grade']))
        return result
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return []
    finally:
        conn.close()


def update_grade(student_id, new_grade):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET grade = ? WHERE id = ?",
            (new_grade, student_id)
        )
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return 0
    finally:
        conn.close()


def delete_failing():
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE grade < ?", (3,))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return 0
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()
    print(add_student('Иванов', 5))
    print(add_student('Петров', 2))
    print(add_student(None, 4))
    print(get_all_students())
    print(update_grade(1, 4))
    print(update_grade(999, 4))
    print(delete_failing())
    print(get_all_students())
