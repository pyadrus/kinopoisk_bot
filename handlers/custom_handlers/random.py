import aiogram.utils.exceptions
import requests
from aiogram import types

from database.database import recording_movies_in_the_database, get_random_id_movies, get_movie_info
from system.dispatcher import dp, bot, API_KEY


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
            except aiogram.utils.exceptions.WrongFileIdentifier:
                print("Неправильный идентификатор файла. Указан URL-адрес http...")
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
        except aiogram.utils.exceptions.BadRequest:
            print("Сообщение с подписью (caption), превышает максимальную допустимую длину")
            random_id_movies = get_random_id_movies()
            movie_info, poster_url = get_movie_info(random_id_movies)
            await message.answer_photo(poster_url, caption=movie_info)


def register_random_movie_command_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command)  # Обработчик команды /random
