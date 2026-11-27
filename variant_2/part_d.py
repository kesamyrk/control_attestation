# --- Часть II, задания 34, 35, 36, 39

# Задание 34
def group_by_first_letter(words):
    """
    >>> group_by_first_letter(['apple', 'banana', 'avocado', 'cherry'])
    {'a': ['apple', 'avocado'], 'b': ['banana'], 'c': ['cherry']}
    >>> group_by_first_letter([])
    {}
    >>> group_by_first_letter(['x'])
    {'x': ['x']}
    """
    result = {}
    for word in words:
        letter = word[0]
        if letter not in result:
            result[letter] = []
        result[letter].append(word)
    return result


# Задание 35
def stats(students):
    """
    >>> stats([('A', 3), ('B', 5), ('C', 4)])
    (3, 5, 4.0)
    >>> stats([('A', 2), ('B', 3), ('C', 4)])
    (2, 4, 3.0)
    >>> stats([])
    (None, None, None)
    """
    if not students:
        return (None, None, None)
    min_grade = students[0][1]
    max_grade = students[0][1]
    total = 0
    for name, grade in students:
        if grade < min_grade:
            min_grade = grade
        if grade > max_grade:
            max_grade = grade
        total += grade
    avg_grade = round(total / len(students), 2)
    return (min_grade, max_grade, avg_grade)


# Задание 36
def unique_words(text):
    """
    >>> unique_words('hello world hello python')
    ['hello', 'world', 'python']
    >>> unique_words('Python python PYTHON')
    ['python']
    >>> unique_words('')
    []
    """
    result = []
    for word in text.lower().split():
        if word not in result:
            result.append(word)
    return result


# Задание 39
def top_authors(books, n):
    """
    >>> top_authors([('A', 'X'), ('B', 'Y'), ('C', 'X'), ('D', 'Z'), ('E', 'X')], 2)
    ['X', 'Y']
    >>> top_authors([('A', 'X'), ('B', 'Y'), ('C', 'X'), ('D', 'Y')], 2)
    ['X', 'Y']
    >>> top_authors([('A', 'X')], 5)
    ['X']
    >>> top_authors([], 3)
    []
    """
    # подсчёт книг у каждого автора
    counts = {}
    for title, author in books:
        if author in counts:
            counts[author] += 1
        else:
            counts[author] = 1

    pairs = []
    for author in counts:
        pairs.append((author, counts[author]))

    # сортировка вставками: по количеству по убыванию, при равенстве по алфавиту
    for i in range(1, len(pairs)):
        current = pairs[i]
        j = i - 1
        while j >= 0 and (pairs[j][1] < current[1] or
                          (pairs[j][1] == current[1] and pairs[j][0] > current[0])):
            pairs[j + 1] = pairs[j]
            j -= 1
        pairs[j + 1] = current

    result = []
    for author, count in pairs[:n]:
        result.append(author)
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
