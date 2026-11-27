# --- Часть II, задание 37: CRUD для таблицы books
import sqlite3

DB_PATH = 'library.db'


def init_db():
    # создание таблицы для проверки, по условию она уже есть
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY, "
            "title TEXT NOT NULL, "
            "author TEXT, "
            "year INTEGER)"
        )
        conn.commit()
    finally:
        conn.close()


def add_book(title, author, year):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return False
    finally:
        conn.close()


def get_books_by_author(author):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, year FROM books WHERE author = ?",
            (author,)
        )
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append((row['id'], row['title'], row['year']))
        return result
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return []
    finally:
        conn.close()


def update_year(book_id, new_year):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET year = ? WHERE id = ?",
            (new_year, book_id)
        )
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return 0
    finally:
        conn.close()


def delete_old_books(before_year):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE year < ?", (before_year,))
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
    print(add_book('Война и мир', 'Толстой', 1869))
    print(add_book('Анна Каренина', 'Толстой', 1877))
    print(add_book('Мёртвые души', 'Гоголь', 1842))
    print(add_book(None, 'Пушкин', 1833))
    print(get_books_by_author('Толстой'))
    print(update_year(1, 1867))
    print(update_year(999, 2000))
    print(delete_old_books(1850))
    print(get_books_by_author('Гоголь'))
