# Задание 34
def intersection(a, b):
    """
    >>> intersection([1, 2, 3, 4], [3, 4, 5, 6])
    [3, 4]
    >>> intersection([1, 1, 2, 2, 3], [2, 3, 3, 4])
    [2, 3]
    >>> intersection([1, 2], [3, 4])
    []
    >>> intersection([], [1, 2])
    []
    """
    result = []
    for x in a:
        # элемент есть во втором списке и ещё не добавлен
        if x in b and x not in result:
            result.append(x)
    return result


# Задание 35
def flatten(lst):
    """
    >>> flatten([1, [2, 3], 4, [5]])
    [1, 2, 3, 4, 5]
    >>> flatten([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> flatten([])
    []
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            for x in item:
                result.append(x)
        else:
            result.append(item)
    return result


# Задание 36
def group_by_parity(numbers):
    """
    >>> group_by_parity([1, 2, 3, 4, 5])
    {'even': [2, 4], 'odd': [1, 3, 5]}
    >>> group_by_parity([2, 4])
    {'even': [2, 4], 'odd': []}
    >>> group_by_parity([])
    {'even': [], 'odd': []}
    """
    result = {'even': [], 'odd': []}
    for n in numbers:
        if n % 2 == 0:
            result['even'].append(n)
        else:
            result['odd'].append(n)
    return result
  
# Задание 37: 
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

# Задание 39
def top_three_by_grade(students):
    """
    >>> top_three_by_grade([('A', 3), ('B', 5), ('C', 4)])
    ['B', 'C', 'A']
    >>> top_three_by_grade([('A', 5), ('B', 5), ('C', 4), ('D', 5)])
    ['A', 'B', 'D']
    >>> top_three_by_grade([('A', 3)])
    ['A']
    >>> top_three_by_grade([])
    []
    """
    top = []
    for name, grade in students:
        # ищем место: после всех, у кого оценка больше или равна
        pos = len(top)
        while pos > 0 and top[pos - 1][1] < grade:
            pos -= 1
        top.insert(pos, (name, grade))
        # храним не больше трёх
        if len(top) > 3:
            top.pop()
    names = []
    for name, grade in top:
        names.append(name)
    return names


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
