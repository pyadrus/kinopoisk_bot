import sqlite3
import random

DATABASE_FILE = 'database.db'  # Имя файла базы данных


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
        # Проверяем, что poster_url не пустой (содержит данные)
        if poster_url:
            return movie_info, poster_url
        else:
            return movie_info, None  # Если poster_url пустой, возвращаем None
    else:
        return None


def get_random_movie_by_ratings(keyword):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Разбиваем входную строку на минимальное и максимальное значение рейтинга
    min_rating, max_rating = map(float, keyword.split('-'))
    # Выбираем случайный фильм с рейтингом в указанном диапазоне
    cursor.execute("SELECT id_movies FROM movies WHERE rating >= ? AND rating <= ?",
                   (min_rating, max_rating))
    matching_movie_ids = cursor.fetchall()
    if not matching_movie_ids:
        conn.close()
        return None  # Фильмов с указанным рейтингом в выбранном диапазоне не найдено
    # Случайный выбор одного из фильмов
    random_movie_id = random.choice(matching_movie_ids)[0]
    # Получаем информацию о фильме
    movie_info, poster_url = get_movie_info(random_movie_id)
    conn.close()
    return movie_info, poster_url


def get_random_movie_by_country(keyword):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id_movies FROM movies WHERE countries LIKE ?", ('%' + keyword + '%',))
    matching_movie_ids = cursor.fetchall()
    conn.close()
    if not matching_movie_ids:
        return None  # Фильмов с указанной страной не найдено
    # Случайный выбор одного из фильмов
    random_movie_id = random.choice(matching_movie_ids)[0]
    print(random_movie_id)
    # Получаем информацию о фильме
    movie_info, poster_url = get_movie_info(random_movie_id)
    return movie_info, poster_url


def get_random_movie_by_genre_and_year(keyword):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Разбиваем входную строку на жанр и диапазон года
    genre, year_range = keyword.split(',')
    # Разбиваем диапазон года на минимальное и максимальное значение
    min_year, max_year = map(int, year_range.split('-'))
    # Выбираем случайный фильм с указанным жанром и годом в указанном диапазоне
    cursor.execute("SELECT id_movies FROM movies WHERE genres LIKE ? AND year BETWEEN ? AND ?",
                   ('%' + genre + '%', min_year, max_year))
    matching_movie_ids = cursor.fetchall()
    if not matching_movie_ids:
        conn.close()
        return None  # Фильмов с указанным жанром и годом в выбранном диапазоне не найдено
    # Случайный выбор одного из фильмов
    random_movie_id = random.choice(matching_movie_ids)[0]
    # Получаем информацию о фильме
    movie_info, poster_url = get_movie_info(random_movie_id)
    conn.close()
    return movie_info, poster_url


def get_random_movie_by_genre_year_rating_country(keyword):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    print(keyword)
    genre,year_range, country,  top_rating = keyword.split(',')
    print(genre, country, year_range, top_rating)
    min_year, max_year = map(int, year_range.split('-'))
    print(min_year, max_year)
    min_rating, max_rating = map(float, top_rating.split('-'))
    print(min_rating, max_rating)
    cursor.execute("SELECT id_movies FROM movies WHERE genres LIKE ? AND year BETWEEN ? AND ? AND rating BETWEEN ? AND ? AND countries LIKE ?",('%' + genre + '%', min_year, max_year, min_rating, max_rating, '%' + country + '%'))
    matching_movie_ids = cursor.fetchall()
    print(matching_movie_ids)
    if not matching_movie_ids:
         conn.close()
         return None  # No movies found with the selected criteria
    random_movie_id = random.choice(matching_movie_ids)[0]
    print(random_movie_id)
    movie_info, poster_url = get_movie_info(random_movie_id)
    conn.close()
    return movie_info, poster_url


def count_rows_in_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Выполните SQL-запрос для подсчета строк в таблице
    cursor.execute(f"SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]  # Получите результат запроса
    conn.close()  # Закройте соединение с базой данных
    return count


if __name__ == '__main__':
    get_random_id_movies()
