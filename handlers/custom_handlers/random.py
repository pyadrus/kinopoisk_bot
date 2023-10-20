import sqlite3
import random
import requests
from aiogram import types
import aiogram.utils.exceptions

from system.dispatcher import dp, bot

# Замените 'YOUR_API_KEY' на ваш реальный ключ API
# API_KEY = '5M8YYRN-5T3MTDZ-MES7BD1-W54W07X'
API_KEY = 'GJ616KK-DPC4PAH-NQVE0SS-K7Y563C'

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


async def get_random_movie(chat_id, api_key):
    url = 'https://api.kinopoisk.dev/v1.3/movie/random'
    headers = {'X-API-KEY': api_key}

    # Показываем индикатор "бот печатает" пользователю
    await bot.send_chat_action(chat_id, 'typing')

    response = requests.get(url, headers=headers, timeout=(10, 30))

    if response.status_code == 200:
        data = response.json()
        print(data)
        id_movies = data.get('id')
        print(id_movies)
        name = data.get('name', 'Название фильма не найдено')
        year = data.get('year', 'Год выпуска не найден')
        rating = data.get('rating', {}).get('kp', 'Рейтинг не найден')
        description = data.get('description', 'Описание не найдено')
        genres = ', '.join([genre.get('name', '') for genre in data.get('genres', [])])
        countries = ', '.join([country.get('name', '') for country in data.get('countries', [])])
        poster_url = data.get('poster', {}).get('url', '')

        movie_info = (f'Название: {name}\n'
                      f'Год выпуска: {year}\n'
                      f'Рейтинг Кинопоиска: {rating}\n'
                      f'Жанры: {genres}\n'
                      f'Страна: {countries}\n\n'
                      f'Описание: {description}\n')
        recording_movies_in_the_database(id_movies, name, year, rating, description, genres, countries, poster_url)
        return movie_info, poster_url
    else:
        return None, None


# Функция для получения случайного id_movies из базы данных
def get_random_id_movies():
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


@dp.message_handler(lambda message: message.text == "Случайный фильм")
async def random_movie_command(message: types.Message):
    # Определите chat_id, чтобы показать индикатор "бот печатает" в нужном чате
    chat_id = message.chat.id
    # Показываем индикатор "бот печатает"
    await bot.send_chat_action(chat_id, 'typing')
    # Получаем информацию о случайном фильме
    movie_info, poster_url = await get_random_movie(chat_id, API_KEY)
    if movie_info:
        if poster_url:
            try:
                await message.answer_photo(poster_url, caption=movie_info)
            except aiogram.utils.exceptions.InvalidHTTPUrlContent:
                print("Ошибка получения содержимого HTTP-URL")
                random_id_movies = get_random_id_movies()
                movie_info, poster_url = get_movie_info(random_id_movies)
                await message.answer_photo(poster_url, caption=movie_info)
            except aiogram.utils.exceptions.BadRequest:
                print("Сообщение с подписью (caption), превышает максимальную допустимую длину")
                random_id_movies = get_random_id_movies()
                movie_info, poster_url = get_movie_info(random_id_movies)
                await message.answer_photo(poster_url, caption=movie_info)

    else:
        try:
            random_id_movies = get_random_id_movies()
            movie_info, poster_url = get_movie_info(random_id_movies)
            await message.answer_photo(poster_url, caption=movie_info)
            # await message.answer("Не удалось получить данные о фильме. Попробуйте ещё раз позже.")
        except aiogram.utils.exceptions.BadRequest:
            print("Сообщение с подписью (caption), превышает максимальную допустимую длину")
            random_id_movies = get_random_id_movies()
            movie_info, poster_url = get_movie_info(random_id_movies)
            await message.answer_photo(poster_url, caption=movie_info)


def register_random_movie_command_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command)  # Обработчик команды /random
