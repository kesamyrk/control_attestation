# --- Часть I, задание 38: маршрут /students
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from students_db import DB_PATH, init_db, get_all_students

app = Flask(__name__)


@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        grade_text = request.form.get('grade', '').strip()

        # валидация
        if not name:
            return render_template('students.html', students=get_all_students(),
                                   error='Имя не может быть пустым')
        try:
            grade = int(grade_text)
        except ValueError:
            return render_template('students.html', students=get_all_students(),
                                   error='Оценка должна быть целым числом')
        if grade < 1 or grade > 5:
            return render_template('students.html', students=get_all_students(),
                                   error='Оценка должна быть от 1 до 5')

        # вставка в базу
        conn = sqlite3.connect(DB_PATH)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, grade) VALUES (?, ?)",
                (name, grade)
            )
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            print(f"[DB ERROR] {e}")
            return render_template('students.html', students=get_all_students(),
                                   error='Не удалось сохранить студента')
        finally:
            conn.close()

        return redirect(url_for('students'))

    # GET: список студентов
    return render_template('students.html', students=get_all_students())


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
