import sqlite3
import random

DATABASE_FILE = 'channels.db'  # Имя файла базы данных


def recording_movies_in_the_database(id_movies, name, year, rating, description, genres, countries, poster_url):
    """Запись фильмов в базу данных"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Проверяем, существует ли запись с таким id_movies
    cursor.execute("SELECT * FROM movies WHERE id_movies = ?", (id_movies,))
    existing_record = cursor.fetchone()

    if existing_record:
        # Запись с таким id_movies уже существует, вы можете решить, что делать с дубликатом
        # Например, вы можете обновить существующую запись или игнорировать дубликат
        # В этом примере, мы игнорируем дубликат
        print(f"Запись с id_movies={id_movies} уже существует. Игнорируем дубликат.")
    else:
        # Запись с id_movies не существует, выполняем вставку
        cursor.execute("INSERT INTO movies (id_movies, name, year, rating, description, genres, countries, poster_url) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (id_movies, name, year, rating, description, genres, countries, poster_url))
        conn.commit()
        print(f"Запись с id_movies={id_movies} успешно добавлена в базу данных.")

    conn.close()

def get_random_id_movies():
    """Функция для получения случайного id_movies из базы данных"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Выбираем все существующие id_movies
    cursor.execute("SELECT id_movies FROM movies")
    id_movies_list = cursor.fetchall()

    conn.close()

    # Если есть хотя бы один id_movies, выбираем случайный из них
    if id_movies_list:
        random_id_movies = random.choice(id_movies_list)[0]
        return random_id_movies
    else:
        return None

def get_movie_info(id_movies):
    """Получение информации о фильме по id_movies"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Выбираем запись по id_movies
    cursor.execute(
        "SELECT name, year, rating, description, genres, countries, poster_url FROM movies WHERE id_movies = ?",
        (id_movies,))
    movie_data = cursor.fetchone()

    conn.close()

    if movie_data:
        name, year, rating, description, genres, countries, poster_url = movie_data
        movie_info = (f'Название: {name}\n'
                      f'Год выпуска: {year}\n'
                      f'Рейтинг Кинопоиска: {rating}\n'
                      f'Жанры: {genres}\n'
                      f'Страна: {countries}\n\n'
                      f'Описание: {description}\n')
        return movie_info, poster_url
    else:
        return None

if __name__ == '__main__':
    get_random_id_movies()