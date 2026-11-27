# --- Часть II, задание 38: маршрут /books с фильтром по автору
from flask import Flask, render_template, request
import sqlite3

from books_db import DB_PATH, init_db

app = Flask(__name__)


@app.route('/books')
def books():
    author = request.args.get('author', '').strip()

    # запрос с фильтром или без
    if author:
        sql = "SELECT id, title, author, year FROM books WHERE author = ?"
        params = (author,)
    else:
        sql = "SELECT id, title, author, year FROM books"
        params = ()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = []
        for row in cursor.fetchall():
            result.append((row['id'], row['title'], row['author'], row['year']))
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[DB ERROR] {e}")
        return render_template('books.html', books=[], author=author,
                               error='Не удалось загрузить книги')
    finally:
        conn.close()

    return render_template('books.html', books=result, author=author)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
